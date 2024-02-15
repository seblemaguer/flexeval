from typing import Dict, List, Set
import itertools
from collections import defaultdict
import math
import random
import threading
import logging

from .System import System
from flexeval.mods.test.model import SampleModel

MUTEX_SELECTION = threading.Semaphore()


class SelectionBase:
    def __init__(
        self,
        systems: Dict[str, System],
        references: List[str] = [],
        include_references: bool = False,
    ):
        self._systems = systems
        self._references = references
        self._include_reference = include_references
        self._logger = logging.getLogger(self.__class__.__name__)

    def select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Select sample method

        This method is a wrapper on _select_samples to ensure an exclusive access to the critical section

        Parameters
        ----------
        user_id : str
            the user ID
        nb_systems : int
            the number of systems
        nb_samples : int
            the number of samples

        Returns
        -------
        Dict[str, List[SampleModel]]
            A dictionnary associating the sample to its ID

        """
        MUTEX_SELECTION.acquire()
        to_return = self._select_samples(user_id, nb_systems, nb_samples)
        MUTEX_SELECTION.release()

        return to_return

    def _select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Select sample method

        This method should be overriden by the subclasses

        Parameters
        ----------
        user_id : str
            the user ID
        nb_systems : int
            the number of systems
        nb_samples : int
            the number of samples

        Returns
        -------
        Dict[str, List[SampleModel]]
            A dictionnary associating the sample to its ID

        """
        raise NotImplementedError(f'The class "{self.__class__.__name__}" should override the method "_select_samples"')


class LeastSeenSelection(SelectionBase):
    """Class implementing the selection strategy based on the "least seen" paradigm:
    1. list the least seen system(s)
    2. for the the least system(s), select the least seen sample(s)
    """

    def __init__(self, systems: Dict[str, System]) -> None:
        """Constructor

        Parameters
        ----------
        systems: Dict[str, System]
            The dictionnary of systems indexed by their names
        """
        super().__init__(systems)

        # Initialize content elements
        self._samples = [sample.id for _, cur_system in systems.items() for sample in cur_system[0].system_samples]

        # Initialize counters
        self._system_counters = defaultdict(0)
        self._sample_counters = defaultdict(0)

    def select_systems(self, nb_systems: int) -> List[str]:
        """Select a certain amount systems among the least seen ones

        Parameters
        ----------
        nb_systems: int
            The desired number of systems for one step

        Returns
        -------
        List[str]
            the list of names of the selected systems
        """

        # Sort systems by descending order of usage
        pool_systems = sorted(self._system_counters.items(), key=lambda item: item[1])

        # Assert/Fix the number of required systems
        assert (nb_systems <= len(pool_systems)) and (nb_systems != 0), (
            f"The required number of systems ({nb_systems}) is greater than the available number of systems "
            + f"({len(pool_systems)}) or it is 0"
        )

        # Preparing pool of systems
        if nb_systems > 0:
            min_count = math.inf
            tmp_pool = []
            for system, count in pool_systems:
                if count > min_count:
                    break

                tmp_pool.append((system, count))
                min_count = count

            pool_systems = tmp_pool

        # Ignore the counting from now, we are only interested with the systems themselves
        pool_systems = [system[0] for system in pool_systems]

        # Shuffle the systems to guarantee variation in the presentation order
        random.shuffle(pool_systems)

        # Select the desired number of systems
        pool_systems = pool_systems[:nb_systems]
        for p in pool_systems:
            self._system_counters[p] += 1

        return pool_systems

    def internal_select_samples(self, system_name: str, nb_samples: int) -> List[SampleModel]:
        """Select a given number of samples of a given system

        Parameters
        ----------
        system_name: str
           The name of the system
        nb_samples: int
           The desired number of sample

        Returns
        -------
        List[SampleModel]
            The list of selected samples
        """
        # Subset the list of samples
        dict_samples = dict([(sample.id, sample) for sample in self._systems[system_name][0].system_samples])
        sample_subset = {sample_id: self._sample_counters[sample_id] for sample_id in dict_samples.keys()}

        # Sort by counting the pool of samples
        pool_samples = sorted(sample_subset.items(), key=lambda item: item[1])

        # Assert/Fix the number of required samples
        assert (nb_samples <= len(pool_samples)) and (nb_samples != 0), (
            f"The required number of samples ({nb_samples}) is greater than the available number of samples "
            + f"({len(pool_samples)}) or it is 0"
        )

        # Preparing pool of samples
        if nb_samples > 0:
            min_count = math.inf  # NOTE: Infinite is hardcoded here!
            tmp_pool = []
            for sample, count in pool_samples:
                if count > min_count:
                    break

                tmp_pool.append((sample, count))
                min_count = count

            pool_samples = tmp_pool

        # Ignore the counting from now, we are only interested with the samples themselves
        pool_samples = [sample[0] for sample in pool_samples]

        # Shuffle the samples to guarantee variation in the presentation order
        random.shuffle(pool_samples)

        # Select the desired number of samples
        pool_samples = pool_samples[:nb_samples]
        for p in pool_samples:
            self._sample_counters[p] += 1

        return [dict_samples[sample_id] for sample_id in pool_samples]

    def _select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Method to select a given number of samples for a given number of systems for a specific user

        The selection strategy is twofold:
           1. select the desired number of least systems
           2. for each selected system, select the least seen samples (the desired number of samples for each system)

        Parameters
        ----------
        user_id: str
            The identifier of the participant
        nb_systems: int
            The desired number of systems
        nb_samples: int
            The desired number of samples

        Returns
        -------
        Dict[str, List[SampleModel]]
            The dictionary providing for a system name the associated sample embedded in a list
        """

        # Select the systems
        self._logger.debug(f"Select systems for user {user_id}")
        pool_systems = self.select_systems(nb_systems)

        self._logger.debug(self._system_counters)

        # Select the samples
        self._logger.debug(f"Select samples for user {user_id}")
        dict_samples = dict()
        for system_name in pool_systems:
            dict_samples[system_name] = self.internal_select_samples(system_name, nb_samples)

        self._logger.info(f"This is what we will give to {user_id}: {dict_samples}")

        return dict_samples


class LatinSquareSystemLeastSeenSampleSelection(LeastSeenSelection):
    """Class implementing the following selection strategy:
    1. Select the systems using the latin square paradigm
    2. for the the selected system(s), select the least seen sample(s)
    """

    def __init__(self, systems: Dict[str, System]) -> None:
        """Constructor

        Parameters
        ----------
        systems: Dict[str, System]
            The dictionnary of systems indexed by their names
        """
        super().__init__(systems)

        # Initialize user/permutation info
        self._user_infos = dict()
        self._current_permutation_idx = 0

        # Generate system permuations based on a latin square
        nb_systems = len(systems.keys())
        permutation_system = [((i + j) % nb_systems) for i in range(nb_systems) for j in range(nb_systems)]

        # Initialize flatten system list based on permutation
        list_system_names = list(systems.keys())
        self._permutation_system_names = []
        for i_perm in permutation_system:
            system_name = list_system_names[i_perm]
            self._permutation_system_names.append(system_name)

    def select_systems(self, user_id: str, nb_systems: int) -> List[str]:
        """Select a certain amount systems using the latin square paradigm

        Parameters
        ----------
        nb_systems: int
            The desired number of systems

        Returns
        -------
        List[str]
            the list of names of the selected systems
        """
        # Create user if not really
        if user_id not in self._user_infos:
            self._user_infos[user_id] = [self._current_permutation_idx, 0]
            self._logger.debug(f"{user_id} has been associated to permutation {self._current_permutation_idx}")
            self._current_permutation_idx += 1

        # Resume position
        cur_position = (self._user_infos[user_id][0] * len(self._systems)) + self._user_infos[user_id][1]

        # Select samples
        pool_systems = []
        shift = 0
        for _ in range(nb_systems):
            system_name = self._permutation_system_names[cur_position % len(self._permutation_system_names)]
            pool_systems.append(system_name)

            self._logger.warning(
                f"{user_id} (with permutation [{self._user_infos[user_id][0]}]) has been selecting couple "
                + f"(cur_pos = {cur_position}, sys={system_name})"
            )

            cur_position += 1
            shift += 1

        # Prepare to move next
        self._user_infos[user_id][1] += shift

        return pool_systems

    def _select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Method to select a given number of samples for a given number of systems for a specific user

        The selection strategy is twofold:
           1. select the desired number of least systems
           2. for each selected system, select the least seen samples (the desired number of samples for each system)

        Parameters
        ----------
        user_id: str
            The identifier of the participant
        nb_systems: int
            The desired number of systems (it should be = 1 )
        nb_samples: int
            The desired number of samples (it should be = 1)

        Returns
        -------
        Dict[str, List[SampleModel]]
            The dictionary providing for a system name the associated sample embedded in a list
        """

        # Select the systems
        self._logger.debug(f"Select systems for user {user_id}")
        pool_systems = self.select_systems(user_id, nb_systems)

        # Select the samples
        self._logger.debug(f"Select samples for user {user_id}")
        dict_samples = dict()
        for system_name in pool_systems:
            dict_samples[system_name] = self.internal_select_samples(system_name, nb_samples)

        self._logger.info(f"This is what we will give to {user_id}: {dict_samples}")

        return dict_samples


class RandomizedBalancedSelection(SelectionBase):
    """Class implementing the selection strategy using a permutation matrix allowing

    For now, this selection strategy is only desined for MOS/CMOS/DMOS
    or any test only presenting one sample to evaluate per step!

    """

    def __init__(self, systems: Dict[str, System]) -> None:
        """Constructor

        Parameters
        ----------
        systems: Dict[str, System]
            The dictionnary of systems indexed by their names
        """

        super().__init__(systems)

        # Initialize content elements
        self._system_names = list(systems.keys())

        # Be sure that the number of samples per systems equal the number of systems
        nb_systems = len(systems.keys())
        for sys_name, cur_system in systems.items():
            assert len(cur_system[0].system_samples) == nb_systems, (
                f'The number of samples ({len(cur_system[0].system_samples)}) for the system "{sys_name}" is different '
                + f"from the number of available systems ({nb_systems})"
            )

        # Initialize user/permutation info
        self._user_infos = dict()
        self._start_idx = 5  # NOTE: hardcoded (aber warum?!)

        # Generate permutation matrix
        self._init_permutations = []
        for i_sys in range(nb_systems):
            for i_utt in range(nb_systems):
                self._init_permutations.append((i_sys, i_utt))

    def _select_samples(self, user_id: str, nb_systems: int = 1, nb_samples: int = 1) -> Dict[str, List[SampleModel]]:
        """Method to select a sample for a system (the parmeters should be set to 1 for both the number of systems
        and the number of samples)

        This method relies on an internal (prefilled) permutation matrix which provides the sequence of samples
        seen by the participant.

        When a new participant is found, the strategy is as follows:
          1. select, based on an incremented index, which permutation to use
          2. shuffle the permutation ()
          3. associate to the participant the shuffled permutation and an index used as an iterator

        In all cases:
          1. fill the needed information to be returned using the permutation and the current index
          2. increment the index associated to the user

        Parameters
        ----------
        user_id: str
            The identifier of the participant
        nb_systems: int
            The desired number of systems (it should be = 1 )
        nb_samples: int
            The desired number of samples (it should be = 1)

        Returns
        -------
        Dict[str, List[SampleModel]]
            The dictionary providing for a system name the associated sample embedded in a list
        """

        assert nb_systems == 1, (
            "RandomizedBalanced selection strategy imposes that the number of systems required per step is 1. "
            + f"The requested number of systems is {nb_systems}."
        )

        assert nb_samples == 1, (
            "RandomizedBalanced selection that the number of requested samples to be 1."
            + f"The requested number of samples is {nb_samples}."
        )

        # Create user if not ready
        if user_id not in self._user_infos:
            # Select permutations
            total_nb_systems = len(self._systems)
            cur_permutation = []
            cur_idx = self._start_idx
            offset = 0

            for _ in range(total_nb_systems):
                cur_permutation.append(self._init_permutations[cur_idx])
                offset += 1
                self._logger.debug(
                    f"boundary = {(cur_idx + 1) % total_nb_systems}, cur_idx = {cur_idx}, "
                    + f"total_nb_systems={total_nb_systems}, len={len(self._init_permutations)}"
                )

                if ((cur_idx + 1) % total_nb_systems) == 0:
                    cur_idx += 1
                else:
                    step = total_nb_systems + 1
                    cur_idx += step

            # Suffle the permutations
            random.shuffle(cur_permutation)

            self._user_infos[user_id] = [cur_permutation, 0]
            self._logger.debug(
                f"{user_id} has been associated to permutation {self._start_idx} with the following "
                + f"permutation (sys_idx, samp_idx): {cur_permutation}"
            )
            self._start_idx += 1
            self._start_idx = self._start_idx % total_nb_systems

        # Retrieve sample
        cur_position = self._user_infos[user_id][1]
        system_idx, sample_idx = self._user_infos[user_id][0][cur_position]

        # Indicate that we move to the next position
        self._user_infos[user_id][1] += 1

        # Fill the dictionnary of samples to return
        dict_samples = dict()
        system_name = self._system_names[system_idx]
        dict_samples[system_name] = [self._systems[system_name][0].system_samples[sample_idx]]

        self._logger.debug(f"This is what we will give to {user_id}: {dict_samples}")
        return dict_samples


class LeastSeenPerUserSelection(LeastSeenSelection):
    """Class implementing the selection strategy based on the "least seen" (user focused) paradigm:
    1. list the least seen system(s)
    2. for the the least system(s), select the least seen sample(s)
    """

    def __init__(self, systems: Dict[str, System]) -> None:
        """Constructor

        Parameters
        ----------
        systems: Dict[str, System]
            The dictionnary of systems indexed by their names
        """
        super().__init__(systems)

        self._user_history = dict()

    def select_user_systems(self, user_history: Dict[str, Set[str]], nb_systems: int) -> List[str]:
        # Get the list of available systems sorted in ascending order
        system_count_list = [(sys_name, len(seen_samples)) for sys_name, seen_samples in user_history.items()]
        system_count_list.sort(key=lambda x: x[1])

        # Get the cutting edge
        cut_idx = 1
        start_count = system_count_list[0][1]
        for cut_idx, cur_elt in enumerate(system_count_list[1:], 1):
            if cur_elt[1] != start_count:
                break

        # Subset and shuffle
        if cut_idx < nb_systems:
            pool_systems = system_count_list[:nb_systems]
        else:
            pool_systems = system_count_list[:cut_idx]
        random.shuffle(pool_systems)

        return [x[0] for x in pool_systems[:nb_systems]]

    def user_select_samples(self, user_history: Set[str], system_name: str, nb_samples: int) -> List[SampleModel]:
        """Select a given number of samples of a given system

        Parameters
        ----------
        system_name: str
           The name of the system
        nb_samples: int
           The desired number of sample

        Returns
        -------
        List[SampleModel]
            The list of selected samples
        """
        # Subset the list of samples
        dict_samples = dict([(sample.id, sample) for sample in self._systems[system_name][0].system_samples])
        sample_subset = {
            sample_id: self._sample_counters[sample_id]
            for sample_id in dict_samples.keys()
            if sample_id not in user_history
        }

        # Sort by counting the pool of samples
        pool_samples = sorted(sample_subset.items(), key=lambda item: item[1])

        # Assert/Fix the number of required samples
        self._logger.debug(f"Number of samples {nb_samples} from a pool of {len(pool_samples)} samples is required")
        assert (nb_samples <= len(pool_samples)) and (nb_samples > 0), (
            f"The required number of samples ({nb_samples}) is greater "
            + f"than the available number of samples {len(pool_samples)} or it is 0"
        )

        # Subset to get the desired number of samples and shuffle to guarantee variation in the presentation order
        # NOTE: to ensure variability, we first need to take into account the pool of samples seens
        #       the same amount of time
        nb_id_samples = 0
        for nb_id_samples in range(1, len(pool_samples)):
            if pool_samples[nb_id_samples - 1][1] != pool_samples[nb_id_samples][1]:
                break

        if nb_id_samples > nb_samples:
            pool_samples = pool_samples[:nb_id_samples]
            random.shuffle(pool_samples)
            pool_samples = pool_samples[:nb_samples]
        else:
            pool_samples = pool_samples[:nb_samples]
            random.shuffle(pool_samples)

        # Select the desired number of samples
        for sample in pool_samples:
            self._sample_counters[sample[0]] += 1
            user_history.add(sample[0])

        return [dict_samples[sample[0]] for sample in pool_samples]

    def _select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Method to select a given number of samples for a given number of systems for a specific user

        The selection strategy is twofold:
           1. select the desired number of least systems
           2. for each selected system, select the least seen samples (the desired number of samples for each system)

        Parameters
        ----------
        user_id: str
            The identifier of the participant
        nb_systems: int
            The desired number of systems
        nb_samples: int
            The desired number of samples

        Returns
        -------
        Dict[str, List[SampleModel]]
            The dictionary providing for a system name the associated sample embedded in a list
        """

        if user_id not in self._user_history:
            self._user_history[user_id] = dict([(cur_system, set()) for cur_system in self._systems.keys()])

        # Select the systems
        self._logger.debug(f"Select systems for user {user_id}")
        pool_systems = self.select_user_systems(self._user_history[user_id], nb_systems)

        # Select the samples
        self._logger.debug(f"Select samples for user {user_id}")
        dict_samples = dict()
        for system_name in pool_systems:
            dict_samples[system_name] = self.user_select_samples(
                self._user_history[user_id][system_name], system_name, nb_samples
            )

        self._logger.info(f"This is what we will give to {user_id}: {dict_samples}")

        return dict_samples


class LeastSeenCombinationSelection(SelectionBase):
    """Class implementing the selection strategy based on the "least seen" paradigm:
    1. list the least seen system(s)
    2. for the the least system(s), select the least seen sample(s)
    """

    SYS_COMB_SEP = ":"

    def __init__(self, systems: Dict[str, System], nb_systems: int) -> None:
        """Constructor

        Parameters
        ----------
        systems: Dict[str, System]
            The dictionnary of systems indexed by their names
        """
        super().__init__(systems)

        self._nb_systems = nb_systems

        # Initialize content elements
        samples = [sample.id for _, cur_system in systems.items() for sample in cur_system[0].system_samples]

        # Initialize counters
        self._system_counters = dict(
            [
                (LeastSeenCombinationSelection.SYS_COMB_SEP.join(cur_system), 0)
                for cur_system in itertools.combinations(systems, nb_systems)
            ]
        )
        self._sample_counters = dict([(cur_sample, 0) for cur_sample in samples])

    def select_systems(self, nb_systems: int) -> List[str]:
        """Select a certain amount systems among the least seen ones

        Parameters
        ----------
        nb_systems: int
            The desired number of systems for one step

        Returns
        -------
        List[str]
            the list of names of the selected systems
        """
        assert (
            nb_systems == self._nb_systems
        ), "For the combination selection strategy, the number of systems should be the same for all the test"

        # Sort systems by descending order of usage
        pool_systems = sorted(self._system_counters.items(), key=lambda item: item[1])

        # Assert/Fix the number of required systems
        assert (nb_systems <= len(pool_systems)) and (nb_systems != 0), (
            f"The required number of systems ({nb_systems}) is greater than the available number of systems "
            + f"({len(pool_systems)}) or it is 0"
        )

        # Preparing pool of systems
        if nb_systems > 0:
            min_count = math.inf
            tmp_pool = []
            for system, count in pool_systems:
                if count > min_count:
                    break

                tmp_pool.append((system, count))
                min_count = count

            pool_systems = tmp_pool

        # Ignore the counting from now, we are only interested with the systems themselves
        pool_systems = [system[0] for system in pool_systems]

        # Shuffle the systems to guarantee variation in the presentation order
        random.shuffle(pool_systems)

        # Select the desired number of systems
        pool_systems = pool_systems[0]
        self._system_counters[pool_systems] += 1
        return pool_systems.split(LeastSeenCombinationSelection.SYS_COMB_SEP)

    def internal_select_samples(self, system_name: str, nb_samples: int) -> List[SampleModel]:
        """Select a given number of samples of a given system

        Parameters
        ----------
        system_name: str
           The name of the system
        nb_samples: int
           The desired number of sample

        Returns
        -------
        List[SampleModel]
            The list of selected samples
        """
        # Subset the list of samples
        dict_samples = dict([(sample.id, sample) for sample in self._systems[system_name][0].system_samples])
        sample_subset = {sample_id: self._sample_counters[sample_id] for sample_id in dict_samples.keys()}

        # Sort by counting the pool of samples
        pool_samples = sorted(sample_subset.items(), key=lambda item: item[1])

        # Assert/Fix the number of required samples
        assert (nb_samples <= len(pool_samples)) and (nb_samples != 0), (
            f"The required number of samples ({nb_samples}) is greater than the available number of samples "
            + f"({len(pool_samples)}) or it is 0"
        )

        # Preparing pool of samples
        if nb_samples > 0:
            min_count = math.inf  # NOTE: Infinite is hardcoded here!
            tmp_pool = []
            for sample, count in pool_samples:
                if count > min_count:
                    break

                tmp_pool.append((sample, count))
                min_count = count

            pool_samples = tmp_pool

        # Ignore the counting from now, we are only interested with the samples themselves
        pool_samples = [sample[0] for sample in pool_samples]

        # Shuffle the samples to guarantee variation in the presentation order
        random.shuffle(pool_samples)

        # Select the desired number of samples
        pool_samples = pool_samples[:nb_samples]
        for p in pool_samples:
            self._sample_counters[p] += 1

        return [dict_samples[sample_id] for sample_id in pool_samples]

    def _select_samples(self, user_id: str, nb_systems: int, nb_samples: int) -> Dict[str, List[SampleModel]]:
        """Method to select a given number of samples for a given number of systems for a specific user

        The selection strategy is twofold:
           1. select the desired number of least systems
           2. for each selected system, select the least seen samples (the desired number of samples for each system)

        Parameters
        ----------
        user_id: str
            The identifier of the participant
        nb_systems: int
            The desired number of systems
        nb_samples: int
            The desired number of samples

        Returns
        -------
        Dict[str, List[SampleModel]]
            The dictionary providing for a system name the associated sample embedded in a list
        """

        # Select the systems
        self._logger.debug(f"Select systems for user {user_id}")
        pool_systems = self.select_systems(nb_systems)
        self._logger.debug(self._system_counters)

        # Select the samples
        self._logger.debug(f"Select samples for user {user_id}")
        dict_samples = dict()
        for system_name in pool_systems:
            dict_samples[system_name] = self.internal_select_samples(system_name, nb_samples)

        self._logger.info(f"This is what we will give to {user_id}: {dict_samples}")

        return dict_samples
