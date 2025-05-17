;; Directory Local Variables            -*- no-byte-compile: t -*-
;; For more information see (info "(emacs) Directory Variables")

(
 (python-mode . ((eval . (when (and (fboundp 'micromamba-envs)
                                    (alist-get "flexeval_env" (micromamba-envs) nil nil #'equal))
                           (micromamba-activate (alist-get "flexeval_env"
                                                           (micromamba-envs)
                                                           nil nil
                                                           #'equal))))))


 ;; (python-mode    . ((dape-command . (debugpy :args ["testing"]))))
 ;; (python-ts-mode . ((dape-command . (debugpy
 ;;                                     :program "flexeval"
 ;;                                     :args [
 ;;                                            "-vv" "-l" "./logs/eval_rcv.log"
 ;;                                            "-i" "0.0.0.0" "-p" "8080"
 ;;                                            "-P"
 ;;                                            "./examples/eval_rcv/structure.yaml"
 ;;                                            ]))))
 )
