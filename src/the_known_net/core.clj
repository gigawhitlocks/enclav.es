(ns the-known-net.core
    (:use [hiccup.core]
          [hiccup.page]
          [compojure core response]
          [ring.adapter.jetty :only [run-jetty]]
          [ring.util.response]
          [ring.middleware file file-info stacktrace reload]
          )

    (:require [compojure.route :as route]))

;Generates HTML header and shit
(defn view-layout [ title & content]
    (html (xhtml-tag "en"
          [:head
                 [:meta {:http-equiv "Content-type"
                         :content "text/html; charset=utf-8"}]
                 [:title ( str "theknown.net" title )]
                 [:script {:src "http://use.edgefonts.net/quattrocento-sans.js"}]
                 [:link {:href "http://theknown.net/main.css" :type "text/css" :rel "stylesheet"} ]
           ]
          [:body content])))


;Generates the site's landing page
(defn landing-page [] 
  (view-layout "" ; first arg is page title
      [:div {:class "content"}
      [:h1 {:class "isinviteonly"} "theknown.net "]
      [:h2 {:class "isinviteonly"} "is invite-only"]
      [:br][:a {:style "position:absolute; bottom:14%" :href "sign-in"} "I have an account or an invitation."]]))


(defn notfounderror-page []
  (view-layout ""
    [:center
     "Page not found."
     [:br][:br]
     [:iframe {:width 560 :height 315 :src "http://www.youtube.com/embed/kxopViU98Xo" :frameborder 0}]]))

;Routes
(defroutes app
    (GET "/"        [] (landing-page))
;   (GET "/sign-in" [] (signin-page)))
    (route/not-found (notfounderror-page)) ; TODO: IMPLEMENT 404 PAGE
)

(defn start-server []
    (run-jetty #'the-known-net.core/app {:port 1337 :join? false}))

(defn -main []
  (start-server))

