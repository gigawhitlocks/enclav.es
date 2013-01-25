(ns the-known-net.styles
    (:require [clj-style.core :as cs]))

; GENERATE CSS IN THIS SECTION

;CSS colors
(def darkgreen "#12795D")
(def lightgreen "#88DDC5")
(def font-family "quattrocento-sans,Helvetica,Arial,sans-serif")
(def darkblue "#164379")


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
    :font-size "4em"])

  (cs/defrule body
   [:body
    :background-color lightgreen
    :margin 0
    :padding 0
    :font-family font-family])

 (cs/defrule content
  [:.content
   :display "block"
   :margin-left "15%"
   :margin-top "10%"])

  (cs/defrule links
   [:a
    :text-decoration "none"
    :color darkblue
    :font-size "2em"
    :font-family font-family])

  (cs/render))
