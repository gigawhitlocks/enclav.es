(ns the-known-net.core
  ; ":use" is deprecated / discouraged
    (:require [compojure.route :as route]
              [compojure.core :refer :all]
              [compojure.response :refer :all]
              [ring.adapter.jetty :refer [run-jetty]]
              [ring.util.response :refer :all]
              [ring.middleware.reload :refer :all]
              [sandbar.core :refer :all]
              [sandbar.stateful-session :refer :all]
              [sandbar.auth :refer :all]
              [sandbar.form-authentication :refer :all]
              [sandbar.validation :refer :all]
              [hiccup.core :refer :all]
              [hiccup.page :refer :all]
              [hiccup.element :refer [link-to]]
              [the-known-net.styles :refer :all]))

; WELCOME TO THEKNOWN.NET'S SOURCE CODE


; THE STATE OF THE PROJECT SECTION:
; 
; 1) Right now everything is in this file. Eventually, things should be broken up.
;    It's going to get unwieldy -fast-. We should discuss how best to do this.
;
; 2) Below we have some CSS that should do for the landing page and the sign-in/up page and any error pages.
; 2.1) moved css to css.clj BOOYAH
;
; 3) We also have routes for those pages.
; 4) POST and shit aren't implemented yet.
; 5) Aww, yeah.


; GENERATE HTML IN THIS SECTION

; Generates the title string for a page

; what ian wrote
;(defn maketitle [input]
;  (if (identical? input "")
;    (str "theknown.net")
;    (str "theknown.net | " input)))
; TODO delete this after you understand the new version

;simpler version using pattern matching
(defn maketitle 
  ([]      (str "theknown.net"))
  ([input] (str "theknown.net | " input)))


; Generates HTML for any page  
(defn view-layout [ title css querytype & content ]
    (html (xhtml-tag "en"
          [:head
                 [:meta {:http-equiv "Content-type" :content "text/html; charset=utf-8"}]
                 [:script {:src "http://use.edgefonts.net/quattrocento-sans.js"}]
                 [:title  (maketitle title) ]
                 [:style {:type "text/css"} css ]]
          [:body 
           content
            
(comment ;this should put a login link on every page if a user is logged in, but isn't working for some reason (TODO)
              [:div (if-let [username (current-username)]
                        (str "You are logged in as " username ". ")
                        (link-to "logout" "Logout"))]
)
           ])))


; TODO we'll need to refactor a lot of our page generation, "seeing patterns" in code
; means we're not abstracting / breaking things down enough
; right now the pattern follows:
; (defn new-page []
;    (view-layout <title> <css> <querytype>
;       (data-view
;          content)))

; all data-view is doing is adding a div around any content, which is necessary
; right now page-404's centering borks if it's inside a "content" div.. some css issues...
(defn data-view [& content]
  [:div {:class "content"}
      content])

;Generates the site's landing page
(defn landing-page [] 
  (view-layout "Welcome" (landingcss) (query :public) ; first arg is page title, 2nd is css, 3rd is auth querytype
      [:div {:class "content"}
              [:h1 {:style "display:inline" } "theknown.net "]
              [:h2 {:style "display:inline" } "is invite-only"]
              [:div (link-to "home" "Home")]
              [:div {:style "position:absolute; bottom:14%"} (link-to "sign-in" "I have an account or an invitation." )]]))

;Generate the page with the login form and the signup form
(defn signin-page []
  (view-layout "Sign in / Sign up" (landingcss) (query :public)
        (data-view 
          [:div "null"])))

;;;;
(defn home-view []
  (view-layout "Home" (landingcss) (query :public)
        (data-view
          [:div (link-to "member" "Member Data")]
          [:div (link-to "admin"  "Admin Data")])))

(defn member-view []
  (view-layout "Member Page" (landingcss) (query :members-only)
        (data-view 
          [:h2 "Members Only"]
          [:div (link-to "home" "Home")])))

(defn admin-view []
  (view-layout "Admin Page" (landingcss) (query :top-secret)
        (data-view 
          [:h2 "SECRETS"])))

(defn permission-denied-view []
  (view-layout "Permission Denied" (landingcss) (query :public)
        (data-view
          [:h2 "Permission Denied"]
          [:div (link-to "home" "Home")])))

;;;;
;404 page
(defn page-404 [] ; renamed because "notfounderror-page" is unwieldy
  (view-layout "Page Not Found" (landingcss) (query :public)
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
(defroutes tkn-routes
    (GET "/"                  [] (landing-page))
    (GET "/sign-in"           [] (signin-page))
    (GET "/home"              [] (home-view))
    (GET "/member"            [] (member-view))
    (GET "/admin"             [] (admin-view))
    (GET "/logout"            [] (logout! {}))
    (GET "/permission-denied" [] (permission-denied-view))
    (route/not-found (page-404)))

(def app
    (-> tkn-routes
      (with-security authenticate)
      wrap-stateful-session))

; run the server
(defn start-server []
    (run-jetty #'the-known-net.core/app {:join? false :port 1337 }))

; main
(defn -main []
    (start-server))
