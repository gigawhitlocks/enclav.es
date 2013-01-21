(ns the-known-net.core
    (:use [hiccup.core] 
          [hiccup.page]
          [ring.adapter.jetty]
          [compojure.core])

    (:require [compojure.route :as route]))

;Generates HTML header and shit
(defn view-layout [ title & content]
    (html (xhtml-tag "en"
          [:head
                 [:meta {:http-equiv "Content-type"
                         :content "text/html; charset=utf-8"}]
                 [:title ( str "theknown.net" title )]
                 [:script {:src "http://use.edgefonts.net/quattrocento-sans.js"}]
                 [:link {:href "http://theknown.net/main.css" :type "text/css" :rel "stylesheet"} ]]
          [:body content])))


;Generates the site's landing page
(defn landing-page [] 
  (view-layout "" ; first arg is page title
      [:h1 {:class "isinviteonly"} "theknown.net "]
      [:h2 {:class "isinviteonly"} "is invite only."]
      [:br][:a {:style "position:absolute; bottom:14%" :href "sign-in"} "I have an account or an invitation."]))


;Routes
(defroutes app
    (GET "/" []
             (landing-page)))
 ;   (GET "/sign-in" [] 
  ;           (signin-page)))

(defn -main []
    (run-jetty #'the-known-net.core/app {:port 1337 :join? true}))

