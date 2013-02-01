(ns cluster.core
  ; ":use" is deprecated / discouraged
    (:require [compojure.route :as route]
              [compojure.core :refer [defroutes GET]]
              [compojure.response]
              [ring.adapter.jetty :refer [run-jetty]]
              [ring.util.response :refer :all]
              [ring.middleware.reload :refer :all]
              [ring.middleware.file :refer [wrap-file]]
              [sandbar.core :refer :all]
              [sandbar.stateful-session :refer :all]
              [sandbar.auth :refer :all]
              [sandbar.forms2 :refer :all]
              [sandbar.form-authentication :refer :all]
              [sandbar.validation :refer :all]
              [hiccup.core :refer :all] ; NOTE: we'll eventually most probably refactor to Enlive
              [hiccup.page :refer :all] ; It's still worth it to be using hiccup now
              [hiccup.element :refer [link-to]]
              [cluster.styles :refer :all]
              [cluster.users :refer :all]
              ))

; WELCOME TO THEKNOWN.NET'S SOURCE CODE


; THE STATE OF THE PROJECT SECTION:
; 
; 1) Right now everything is in this file. Eventually, things should be broken up.
;    It's going to get unwieldy -fast-. We should discuss how best to do this.
; 1.1) we'll want to follow MVC or MVP (Model View Presenter) and break up our sorce based on that
;      ie: model is 1 file, presenter is 1 file, view is 1 file.. or something...
;
; 3) We also have routes for those pages.
; 4) POST and shit aren't implemented yet.
; 5) Aww, yeah.


; GENERATE HTML IN THIS SECTION

; Generates the title string for a page
(defn maketitle 
  ([]      (str "cluster.im"))
  ([input] (str "cluster.im | " input)))

; Protects a page based on its querytype
(defn query [type]
  (ensure-any-role-if (= type :admin-only) #{:admin}
                      (= type :member-only) #{:member}
                      (str (name type) " data")))

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
(comment ; why the crap doesn't this work...
            [:br]
            [:div
             (cond (any-role-granted? :admin)
                   "If you can see this then you are an admin!"
                   (any-role-granted? :member)
                   "If you can see this then you are a member!"
                   :else "Click on one of the links above to log in.")]
            [:div (if (any-role-granted? :user :admin)
                    [:div 
                      (str "You are logged in as " (current-username) ". ")
                      (link-to "/logout" "Logout")])]
)
           ])))



; TODO we'll need to refactor a lot of our page generation, "seeing patterns" in code
; means we're not abstracting / breaking things down enough
; I imagine this is where a macro would come in handy

; DRY (Don't Repeat Yourself) vs. WET (Write Everything Twice) :P

; right now the pattern follows:
; (defn new-page []
;    (view-layout <title> <css> <querytype>
;       (data-view
;          content)))

; all data-view is doing is adding a div around any content, which is necessary
; right now page-404's centering borks if it's inside a "content" div.. these are largely css issues.
(defn data-view [& content]
  [:div {:class "content"}
      content])

(defn title-view [& content] ; similar to data-view, but adds the site's generic title
  [:div {:class "content"}
      [:h1 {:style "display:inline" } "cluster.im "]
      content])

;Generates the site's landing page
(defn landing-page [] 
  (view-layout "Welcome" (landingcss) (query :public) ; first arg is page title, 2nd is css, 3rd is auth querytype
      [:div {:class "content"}
              [:h1 {:style "display:inline" } "cluster.im "]
              [:h2 {:style "display:inline" } "is invite-only"]
              [:div {:style "position:absolute; bottom:14%"} (link-to "sign-in" "I have an account or an invitation." )]]))

;Generate the page with the login form and the signup form
(defn signin-page []
  (view-layout "Sign in / Sign up" (landingcss) (query :public)
        (title-view 
          [:div (link-to "member" "Member Data")]
          [:div (link-to "admin"  "Admin Data")]
          [:div {:style "position:absolute; bottom:14%"} (link-to "/" "Front Page")])))

(defn member-view []
  (view-layout "Member Page" (landingcss) (query :member-only)
        (title-view 
          [:h2 "Members Only"]
          [:div {:style "position:absolute; bottom:14%"} (link-to "/" "Front Page")])))

(defn admin-view []
  (view-layout "Admin Page" (landingcss) (query :admin-only)
        (title-view 
          [:h2 "SECRETS"])))

(defn permission-denied-view []
  (view-layout "Permission Denied" (landingcss) (query :public)
        (title-view
          [:h2 "Permission Denied"]
          [:div {:style "position:absolute; bottom:14%"} (link-to "/" "Front Page")])))

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

; session auth
(defn authenticate [request]
  (let [uri (:uri request)]
    (cond (= uri "/member") {:name "member" :roles #{:member}}
          (= uri "/admin")  {:name "admin" :roles #{:admin}})))

; Routes
(defroutes cluster-routes
    (GET "/"                  [] (landing-page))
    (GET "/sign-in"           [] (signin-page))
    (GET "/member"            [] (member-view))
    (GET "/admin"             [] (admin-view))
    (GET "/logout"            [] (logout! {}))
    (GET "/permission-denied" [] (permission-denied-view))
    (route/not-found (page-404)))

; Hmm, yes, quite stateful indeed.
(def app
    (-> cluster-routes
      (with-security authenticate)
      wrap-stateful-session
      ))

; Run the server
(defn start-server []
    (run-jetty #'cluster.core/app {:join? false :port 1337 }))

; Main
(defn -main []
    (start-server))
