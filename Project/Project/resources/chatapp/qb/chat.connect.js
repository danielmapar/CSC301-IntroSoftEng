//password = current_session.token;
/*QB.chat.connect({jid: jid, password: "password"}, function(err, roster) {
  console.log("Err:", err);
  console.log("Roster:", roster);
});*/




chan_user_id = 1746049;
jid = chan_user_id + "-" + CONFIG.appId + "@chat.quickblox.com";

QB.chat.send(jid, {
    type: 'chat',
    body: 'ping!',

    // any custom parameters
    extension: {
        interests : ["stuff", "and", "things"]
    }
});





QB.chat.addListener({}, function(result) {
    console.log("BOOM!");
    console.log(result);
});

QB.chat.onMessageListener = function(userId, message) {
  console.log("We got a message.");
  console.log("userId:", userId);
  console.log("message:", message);
};