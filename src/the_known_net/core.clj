(ns the-known-net.core
    (:use [hiccup.core]
          [hiccup.page]
          [compojure core response]
          [ring.adapter.jetty :only [run-jetty]]
          [ring.util.response]
          [ring.middleware file file-info stacktrace reload])
    (:require [clj-style.core :as cs])
    (:require [compojure.route :as route]))




; GENERATE CSS IN THIS SECTION

;CSS colors
(def darkgreen "#12795D")
(def lightgreen "#88DDC5")
(def font-family "quattrocento-sans,Helvetica,Arial,sans-serif")
(def darkblue "#164379")


; CSS for the landing page/signin page/login page
(defn landingcss [] 
  (cs/defrule h1landing
   [:h1 
    :color darkgreen
    :margin 0
    :font-size "5em"])

  (cs/defrule h2landing
   [:h2
    :color darkgreen
    :margin 0
    :font-size "4em"])

  (cs/defrule bodylanding
   [:body
    :background-color lightgreen
    :margin 0
    :padding 0
    :font-family font-family])

 (cs/defrule contentlanding
  [:.content
   :display "block"
   :margin-left "15%"
   :margin-top "10%"])

  (cs/defrule linklanding
   [:a
    :text-decoration "none"
    :color darkblue
    :font-size "2em"
    :font-family font-family])

  (cs/render))

; GENERATE HTML IN THIS SECTION

; Generates the title string for a page
(defn maketitle [input]
  (if (identical? input "")
    (str "theknown.net")
    (str "theknown.net | " input)))


; Generates HTML for any page  
(defn view-layout [ title css & content ]
    (html (xhtml-tag "en"
          [:head
                 [:meta {:http-equiv "Content-type"
                         :content "text/html; charset=utf-8"}]
                 [:script {:src "http://use.edgefonts.net/quattrocento-sans.js"}]

                 [:title  (maketitle title) ]

                 [:style {:type "text/css"} css ]
           ]
          [:body content])))

;Generates the site's landing page
(defn landing-page [] 
  (view-layout "" (landingcss) ; first arg is page title ;second is css
      [:div {:class "content"}
      [:h1 {:class "isinviteonly" :style "display:inline" } "theknown.net "]
      [:h2 {:class "isinviteonly"} "is invite-only"]
      [:br][:a {:style "position:absolute; bottom:14%" :href "sign-in"} "I have an account or an invitation." ]]))


;Generate the page with the login form and the signup form
(defn signin-page []
  (view-layout "Sign in / Sign up" (landingcss)
               ))


;404 page
(defn notfounderror-page []
  (view-layout "Page Not Found." (landingcss)
    [:center
     [:br][:br][:br]
     [:h1 "404"
      [:br][:br] ; the youtube video is the sax guy
      [:iframe {:width 560 :height 315 :src "http://www.youtube.com/embed/kxopViU98Xo" :frameborder 0}]
      [:br][:br]
      "FILE NOT FOUND BRO"]]))

;Routes
(defroutes app 
    (GET "/"        [] (landing-page))
     (GET "/sign-in" [] (signin-page))
    (route/not-found (notfounderror-page)) ; TODO: IMPLEMENT 404 PAGE
)


;run the server; main
(defn start-server []
    (run-jetty #'the-known-net.core/app {:port 1337 :join? false}))

(defn -main []
  (start-server))

