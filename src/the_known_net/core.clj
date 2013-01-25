(ns the-known-net.core
  ; ":use" is deprecated / discouraged

    (:require [compojure.route :as route]
              [compojure.core :refer :all]
              [compojure.response :refer :all]
              [ring.adapter.jetty :refer [run-jetty]]
              [ring.util.response :refer :all]
              [ring.middleware.reload :refer :all]
              [hiccup.core :refer :all]
              [hiccup.page :refer [xhtml-tag]]
              [hiccup.element :refer [link-to]]
              [sandbar.core :refer :all]
              [sandbar.auth :refer [with-security]]
              [sandbar.stateful-session :refer [wrap-stateful-session]]
              [the-known-net.styles :refer :all]
              ))

; WELCOME TO THEKNOWN.NET'S SOURCE CODE


; THE STATE OF THE PROJECT SECTION:
; 
; 1) Right now everything is in this file. Eventually, things should be broken up.
;    It's going to get unwieldy -fast-. We should discuss how best to do this.
;
;
; 2) Below we have some CSS that should do for the landing page and the sign-in/up page and any error pages.
; 2.1) moved css to css.clj BOOYAH
;
; 3) We also have routes for those pages.
; 4) POST and shit aren't implemented yet.
; 5) Aww, yeah.


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
                 [:meta {:http-equiv "Content-type" :content "text/html; charset=utf-8"}]
                 [:script {:src "http://use.edgefonts.net/quattrocento-sans.js"}]
                 [:title  (maketitle title) ]
                 [:style {:type "text/css"} css ]]
          [:body content])))

;Generates the site's landing page
(defn landing-page [] 
  (view-layout "" (landingcss) ; first arg is page title ;second is css
      [:div {:class "content"}
      [:h1 {:style "display:inline" } "theknown.net "][:p]
      [:h2 {:style "display:inline" }"is invite-only"]
      [:br][:a {:style "position:absolute; bottom:14%" :href "sign-in"} "I have an account or an invitation." ]]))

;Generate the page with the login form and the signup form
(defn signin-page []
  (view-layout "Sign in / Sign up" (landingcss)
               ))

;;;;
(defn query [type]
  (str (name type) " data"))

(defn layout [content]
  (html
    [:html
     [:body
      [:h2 "test page title"]
      content]]))

(defn data-view [title data & links]
  [:div
   [:h3 title]
   [:p data]
   (if (seq links) links [:div (link-to "home" "Home")])])

(defn home-view []
  (data-view "Home"
             (query :public)
             [:div (link-to "member" "Member data")]
             [:div (link-to "admin"  "Admin dat")]))

(defn member-view []
  (data-view "Member page"
             (query :members-only)))

(defn admin-view []
  (data-view "Admin page"
             (query :top-secret)))


;;;;
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

;stateful session stuff

(defn authenticate [request]
  (let [uri (:uri request)]
    (cond (= uri "/member") {:name "joe" :roles #{:member}}
          (= uri "/admin")  {:name "sue" :roles #{:member}})))

;Routes
(defroutes app
    (GET "/"        [] (landing-page))
    (GET "/sign-in" [] (signin-page))
    (GET "/home*"   [] (layout (home-view)))
    (GET "/member*" [] (layout (member-view)))
    (GET "/admin*"  [] (layout (admin-view)))
    (route/not-found (notfounderror-page)) ; TODO: IMPLEMENT 404 PAGE
)

(comment
(defn app
    (-> tkn-routes
      (with-security authenticate)
      wrap-stateful-session))
)

;run the server
(defn start-server []
    (run-jetty #'the-known-net.core/app {:port 1337 :join? false}))

; main
(defn -main []
    (start-server))
