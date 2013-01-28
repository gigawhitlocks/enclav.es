(defproject the-known-net "0.0.1"
    :description "An experimental online meta-community."
    :plugins [[lein-ring "0.8.2"]]
    :dependencies
      [[org.clojure/clojure "1.4.0"]
            [ring "1.1.8"]
            [ring/ring-devel "1.1.0"]
            [compojure "1.1.5"]
            [hiccup "1.0.2"]
            [org.clojars.cjschroed/sandbar "0.4.3"]
            [korma "0.3.0-RC2"] 
            [postgresql "9.1-901.jdbc4"]
            [clj-style "1.0.1"]]
    :dev-dependencies
      [[lein-run "1.0.0-SNAPSHOT"]
       [lein-diagnosics "0.0.1"]]
    :ring {:handler the-known-net.core/app
           :auto-reload? true
           :auto-refresh? true}
    ; jvm tweaks mostly borrowed from Overtone's project.clj
    :jvm-opts ["-Xms1g" "-Xmx2g"              ; min and max heap sizes
               "-XX:+UseParNewGC"             ; use newer parallel GC with
               "-XX:+UseConcMarkSweepGC"      ;  the concurrent garbage collector
               "-XX:+CMSConcurrentMTEnabled"  ; enable muli-threaded concurrent GC work
               "-XX:MaxGCPauseMillis=20"      ; specify target of 20ms for max GC pauses
               "-XX:+CMSIncrementalMode"      ; do many small GC cycles to minimize pauses
               "-XX:MaxNewSize=256m"
               "-XX:NewSize=257m"
               ]
    :main the-known-net.core)
