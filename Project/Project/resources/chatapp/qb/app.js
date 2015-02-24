var current_session;
var current_user_obj;
var all_users_list;
var message_store = {};
var conversation_box;
var recipient_box;
var message_text_box;

$(document).ready(function() {
    console.log("### document.ready()");
    console.log("CONFIG: ", CONFIG);

    // -------------- Init misc. vars -----------------

    conversation_box = $("#messages");
    recipient_box = $("#recipient_box");
    message_text_box = $("#message_box");

    // -------------- Event handlers ------------------

    $("#create_user_button").click(create_user_button_clicked);
    $("#login_button").click(login_button_clicked);
    $("#send_message_button").click(send_message_button_clicked);
    message_text_box.keypress(function(e){
        if(e.keyCode==13) {
            send_message_button_clicked();
        }
    });
    recipient_box.change(recipient_change_handler);

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

            // Create User
            create_user(user_username, 'password');
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

        var iz_cool = 0;

        if (err) {
            console.log(err);
            var details = JSON.parse(err.detail); //wtf
            console.log(details);
            if (details.hasOwnProperty('errors') &&
                details.errors.hasOwnProperty('login') &&
                details.errors.login[0] == "has already been taken") {
                iz_cool = 1;
            } else {
                alert("Error creating user.");
            }
        } else {
            console.log("User", username, "created.");
            iz_cool = 1;
        }

        console.log("iz_cool: " + iz_cool);

        if (iz_cool == 1) {
            login(user_username, 'password');
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

            $("#title").text("Logged in as " + current_user_obj.login);

            // show message box
            populate_users_list();

            // connect to chat service
            QB.chat.connect({jid: get_my_jid(), password: current_user_password}, function(err, roster) {
            console.log("### QB.chat.connect");

            if (err) {
                alert("Error connecting to chat service.");
                console.log(err.detail);
            } else {
                console.log("Successfully connected to chat service.");
                console.log("Roster:", roster);

                // add message listener
                QB.chat.onMessageListener = message_received_listener;
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
            var id = item.user.id;
            console.log("login: " + login);
            console.log("id: " + id);
            if (login != current_user_obj.login &&
                id != CONFIG.qb_admin_id) {
                // should be using templates..
                html += '<option value="'+login+'">'+login+"</option>";
            }
        });

        recipient_box.html(html);

      }

    });
}

function message_received_listener(userId, message) {
    var from_user = get_username_from_id(userId);
    console.log("We got a message from " + from_user + " (id: " + userId + "):");
    console.log("message:", message);

    // Just in case.
    // seemed like we were getting our own messages
    // TODO: add case for message type != chat
    if (userId != current_user_obj.id && message.type == "chat") {
        add_message(from_user, from_user, message.body);
        display_message(from_user, message.body);
    } else {
        console.log("Wat.");
    }
}

function send_message_button_clicked() {
    console.log("### send_message_button.click");

    // Get recipient user and message
    var user = recipient_box.val().trim();
    var message = message_text_box.val().trim();

    if ( message == "" ) {
        return;
    }

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
    });

    add_message(user, user_username, message);
    display_message(user_username, message);

    message_text_box.get(0).value = "";
}

function recipient_change_handler() {
    console.log("### recipient_change_handler");

    var username = recipient_box.val();

    console.log("Selected user changed to: " + username);

    // clear convo box and fill with chat history
    conversation_box.html("");

    var messages = get_messages_for_user(username);

    messages.forEach(function (m_obj) {
        display_message(m_obj.username, m_obj.message);
    });

}

// Methods to do with managing the message store

function get_username_from_id(user_id) {
    var username = "";

    all_users_list.forEach(function(item) {
        var login = item.user.login;
        var id = item.user.id;
        if (id == user_id) {
            username = login;
        }
    });

    return username;
}

function add_message(convo_user, message_author, message) {
    // convo_user is who's convo you want to store it under
    // message_author is... the author of the message...

    if ( !message_store.hasOwnProperty(convo_user) ) {
        message_store[convo_user] = [];
    }

    message_info = {
        "username" : message_author,
        "message" : message
    };

    message_store[convo_user].push(message_info);
}

function display_message(username, message) {
    var html = conversation_box.html();
    var s = "<li>" + username + ": " + message + "</li>";

    conversation_box.html(html + s);

    // scroll to bottom
    objDiv = conversation_box.get(0);
    objDiv.scrollTop = objDiv.scrollHeight;
}

function get_messages_for_user(username) {
    if ( !message_store.hasOwnProperty(username) ) {
        return [];
    } else {
        return message_store[username];
    }

}
