'use strict';
const {dialogflow} = require('actions-on-google');
const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp()
const app = dialogflow({debug: true});
const db = admin.database();


app.intent('askMenu',(conv,{structure, menucheck}) =>{
    var ref = db.ref("structure/"+`${structure}`);//+`${menucheck}`
    var userRef = ref.child(`${menucheck}`);
    var tmp = "";
    return userRef.once('value').then(function(snapshot) {
        return snapshot.forEach(function(childSnapshot){
            var key = childSnapshot.key;
            var item = childSnapshot.val();
            //tmp.concat(`${key}`,"는",`${item}`,'.\n');
            conv.close(`${structure}`+"의 "+`${menucheck}`+"메뉴입니다. "+ `${key}`+"은 "+`${item}`+" 입니다.");

            //tmp += (`${structure}`+"의 메뉴입니다. "+ `${key}`+"은 "+`${item}`+" 입니다.\n");

            return;
        });

    });

});

exports.NewAgent = functions.https.onRequest(app);
