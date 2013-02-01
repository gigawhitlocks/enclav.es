(ns cluster.styles
    (:require [clj-style.core :as cs]))

; GENERATE CSS IN THIS SECTION

(def font-family "quattrocento-sans,Helvetica,Arial,sans-serif")
(def darkgreen "#006633")
(def lightgreen "#66CC99")
(def darkblue "#003366")
(def red "#CC3333")

; CSS for the landing page/signin page/login page
(defn landingcss [] 
  (cs/defrule h1
   [:h1 
    :color darkgreen
    :margin 0
    :font-size "5em"])

  (cs/defrule h2
   [:h2
    :color darkgreen
    :margin 0
    :font-size "3.5em"])

  (cs/defrule body
   [:body
    :background-color lightgreen
    :margin 0
    :padding 0
    :font-family font-family])

 (cs/defrule content
  [:.content
   :display "block"
   :margin-left "10%"
   :margin-top "10%"])

  (cs/defrule links
   [:a
    :text-decoration "none"
    :color darkblue
    :font-size "2em"
    :font-family font-family])

  (cs/render))
