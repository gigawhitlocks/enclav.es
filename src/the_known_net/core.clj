(ns the-known-net.core
    (:use compojure.core)
    (:use hiccup.core)
    (:use hiccup.page-helpers)
    (:use ring.adapter.jetty))

(defn view-layout [& content]
    (html
          (doctype :xhtml-strict)
          (xhtml-tag "en"
                           [:head
                                    [:meta {:http-equiv "Content-type"
                                                            :content "text/html; charset=utf-8"}]
                                    [:title "theknown.net"]
                                    [:link {:href "http://theknown.net/main.css" :type "text/css" :rel "stylesheet"} ]]
                           [:body content])))

(defn view-input []
    (view-layout
          [:h2 "add two numbers"]
          [:form {:method "post" :action "/"}
                 [:input.math {:type "text" :name "a"}] [:span.math " + "]
                 [:input.math {:type "text" :name "b"}] [:br]
                 [:input.action {:type "submit" :value "add"}]]))

(defn view-output [a b sum]
    (view-layout
          [:h2 "two numbers added"]
          [:p.math a " + " b " = " sum]
          [:a.action {:href "/"} "add more numbers"]))

(defn parse-input [a b]
    [(Integer/parseInt a) (Integer/parseInt b)])

(defn landing-page [] 
  (view-layout
      [:h1 "theknown.net"]
      [:h2 "is invite only."]
      [:a {:href "sign-in"} "I have an account or an invitation."]))

(defn signup []
  [:div {:class "signup"}
   [:form {:method "post" :action "/signup"}
    [:input.text

(defn signin-page [] 
  (view-layout
          (signup)
          (signin)))


(defroutes app
    (GET "/" []
             (landing-page))
    (GET "/sign-in" [] 
             (signin-page)))
;:w
;
;    (POST "/" [a b]
;              (let [[a b] (parse-input a b)
;                              sum   (+ a b)]
;                      (view-output a b sum))))

;(defn -main [] (run-jetty {:port 1337}))
(defn -main []
    (run-jetty #'the-known-net.core/app {:port 1337 :join? true}))
