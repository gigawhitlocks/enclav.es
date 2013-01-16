(ns the-known-net.core
  (:use ring.adapter.jetty))

 
(defn handler [req]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body "Hello Clojure Web!"})

(run-jetty handler {:port 1337})

