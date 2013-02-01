(ns cluster.db
  (:require [korma.db :refer :all]
            [clojure.string :as string]))

(defdb devel (postgres {:db "clusterim-devel"
                        :user "clusterim"
                        :password "54WER12cpdjfu%$@"
                        :host "localhost"
                        :port "5432"
                        :delimiters ""
                        :naming {:keys string/lower-case
                                 :fields string/upper-case}}))

