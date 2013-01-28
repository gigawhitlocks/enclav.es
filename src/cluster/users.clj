(ns cluster.users
  (:require [korma.core :refer :all]
            [the-known-net.db :refer :all]))


(defentity email)
(defentity firstID)
(defentity handle)
(defentity realname)
(defentity sex)
(defentity subscription)
(defentity friend)


(defentity users
  (pk :jid) ; primary key
  (table :users) ; table name
  (entity-fields :jid :realname :handle :subscription :friend)
  (database devel)
  (has-one email)
  (has-one firstID)
  (has-many handle)
  (has-one realname)
  (has-one sex)
  (has-many subscription {:fk :channelID})
  (has-many friend {:fk :jid}))
