var current_session;
var current_user_obj;
var current_user_password; // lolz... need to figure out token auth
var all_users_list;

$(document).ready(function() {
    console.log("### document.ready()");
    console.log("CONFIG: ", CONFIG);

    // -------------- Event handlers ------------------

    $("#create_user_button").click(create_user_button_clicked);
    $("#login_button").click(login_button_clicked);
    $("#send_message_button").click(send_message_button_clicked);

    // ----------------------------- ------------------

    // Init framework
    console.log("Init framework...");
    QB.init(CONFIG.appId, CONFIG.authKey, CONFIG.authSecret, CONFIG.debug);

    // Create app session
    // TODO: necessary? Probs, but double check
    QB.createSession(function (err, result) {
        console.log("### QB.createSession");
        if (err) {
            alert("Error creating session.");
            console.log(err.detail);
        } else {
            console.log("session created.");
            console.log("Result: ", result);
            current_session = result;
        }
    });


});

function get_jid(user_obj) {
    return user_obj.id + "-" + CONFIG.appId + "@chat.quickblox.com";
}

function get_my_jid() {
    return get_jid(current_user_obj);
}

function create_user(username, password) {
    console.log("### create_user");
    console.log("username: '" + username + "'");
    console.log("password: '" + password + "'");

    var params = {login: username, password: password};
    QB.users.create(params, function(err, result) {
        console.log("### QB.users.create");
        console.log("Params:", params);

        if (err) {
            alert("Error creating user.");
            console.log(err.detail);
        } else {
            console.log("User", username, "created.");

            login(username, password);
        }
    });
}

function create_user_button_clicked() {
    console.log("### create_user.click");

    // Get username and pass
    var username = $("#username_box").val();
    var password = $("#password_box").val();

    // Create user
    create_user(username, password);
}

function login(username, password) {
    console.log("### login");
    console.log("username: '" + username + "'");
    console.log("password: '" + password + "'");

    var params = {login: username, password: password};
    QB.login(params, function(err, result) {
        console.log("### QB.login");
        console.log("Params:", params);

        if (err) {
            alert("Error logging in.");
            console.log(err.detail);
        } else {
            console.log("Logged in as user", username);
            console.log("Result:", result);

            current_user_obj = result;
            current_user_password = password;

            // hide login box
            $("#login").hide();
            $("#title").text("Logged in as " + current_user_obj.login);

            // show message box
            populate_users_list();
            $("#text_box").show();

            // connect to chat service
            QB.chat.connect({jid: get_my_jid(), password: current_user_password}, function(err, roster) {
            console.log("### QB.chat.connect");

            if (err) {
                alert("Error connecting to chat service.");
                console.log(err.detail);
            } else {
                console.log("Successfully connected to chat service.");
                console.log("Roster:", roster);

                // show messages box
                msg_box = $("#messages").show();

                // add message listener
                QB.chat.onMessageListener = function(userId, message) {
                    console.log("We got a message from " + userId + ":");
                    console.log("message:", message);

                    // Just in case.
                    // seemed like we were getting our own messages
                    if (userId != current_user_obj.id) {
                        html = msg_box.html();
                        s = "<li>"+userId+": "+message.body+"</li>";

                        msg_box.html(s + html);
                    } else {
                        alert("wat.");
                    }


                };

            }

            });

        }
    });
}

function login_button_clicked() {
    console.log("### login.click");

    // Get username and pass
    var username = $("#username_box").val();
    var password = $("#password_box").val();

    login(username, password);
}

function populate_users_list() {
    console.log("### populate_users_list");

    var params = {
      order: { sort: 'desc', field: 'id' }
    };

    QB.users.listUsers(params, function(err, response){
      console.log("### QB.users.listUsers");
      console.log("Params:", params);

      if (err) {
        alert("Error getting user list.")
        console.log(err.detail);
      } else {
        console.log("Response:", response);

        all_users_list = response.items;

        // populate dropdown with users
        html = "";
        all_users_list.forEach(function(item) {
            var login = item.user.login;
            console.log(login);
            if (login != current_user_obj.login) {
                // should be using templates..
                html += '<option value="'+login+'">'+login+"</option>";
            }
        });

        $("#recipient_box").html(html);

      }

    });
}

function send_message_button_clicked() {
    console.log("### send_message_button.click");

    // Get recipient user and message
    var user = $("#recipient_box").val();
    var message = $("#message_box").val();

    console.log("User: " + user + " | Message: " + message);

    // get user obj
    user_obj = all_users_list.filter(function(e) {
        return e.user.login == user;
    });

    user_obj = user_obj[0].user; // derp.

    console.log("user_obj:", user_obj);
    console.log("user jid:", get_jid(user_obj));

    QB.chat.send(get_jid(user_obj), {
        type: 'chat',
        body: message,

        // any custom parameters
        extension: {
            interests : ["stuff", "and", "things"]
        }
    });

}