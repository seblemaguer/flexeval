
from typing import Dict, List, Any

import random
import logging

from .System import System



class FirstServerSelection:
    def __init__(self, systems: Dict[str, System]) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        # Initialize content elements
        self._systems = systems
        samples = [sample.id for _, cur_system in systems.items() for sample in cur_system[0].system_samples]

        # Initialize counters
        self._system_counters = dict([(cur_system, 0) for cur_system in systems.keys()])
        self._sample_counters = dict([(cur_sample, 0) for cur_sample in samples])


    def select_systems(self, nb_systems: int) -> List[str]:
        self._logger.debug(self._system_counters)

        # Sort systems by descending order of usage
        pool_systems = sorted(self._system_counters.items(), key=lambda item: item[1])

        # Assert/Fix the number of required systems
        assert (nb_systems < len(pool_systems)) and (nb_systems != 0), \
            f"The required number of systems ({nb_systems}) is greater than the available number of systems {len(pool_systems)} or it is 0"

        # Preparing pool of systems
        if nb_systems > 0:
            min_count = 9999999 # NOTE: Infinite is hardcoded here!
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

    def select_samples(self, system_id: str, nb_samples: int) -> List[Any]:

        # Subset the list of samples
        dict_samples = dict([(sample.id, sample) for sample in self._systems[system_id][0].system_samples])
        sample_subset = {sample_id: self._sample_counters[sample_id] for sample_id in dict_samples.keys()}

        # Sort by counting the pool of samples
        pool_samples = sorted(sample_subset.items(), key=lambda item: item[1])


        # Assert/Fix the number of required samples
        assert (nb_samples < len(pool_samples)) and (nb_samples != 0), \
            f"The required number of samples ({nb_samples}) is greater than the available number of samples {len(pool_samples)} or it is 0"

        # Preparing pool of samples
        if nb_samples > 0:
            min_count = 9999999 # NOTE: Infinite is hardcoded here!
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
