# CRC Cards

### Class Name: User
##### Responsibilities:
* update user info
* delete user info
* interests
* list of accepted matches

##### Collaborators:
* Match
* DAO
* Interests

### Class Name: Interests
##### Responsibilities
* list of all interests for a users
* compare 2 interest objects and return value for number of like interests

##### Collaborators:
* User

### Class Name: Match
##### Responsibilities
* status of match between two users
* accept match
* reject match
* block
* link to you and other user

##### Collaborators:
* User

### Class Name: Database Access Object (DAO) [Interface]
##### Responsibilities
* Create user instances
* Create user pairings (matches)

##### Collaborators:
* API
* User
* Match

### Class Name: API
##### Responsibilities
* handle all front end calls
* link front end requests to backend methods
* get and edit user info
* get random potential matches
* accept/reject match
* get list of matches
* start a chat

##### Collaborators:
* DAO
* User
* Match

# CRC Card "walkthroughs"

User story:
As a curious student, I would like to be able to join the service by making a new profile.

Walkthrough:
The frontend web app would call a method in API, such as createAccount which passes in all the profile data. The API class would then create a User object with the data, and pass it on to the DAO which would create a corresponding entry in the database. 

User story:
As a lonely student with bizarre interests, I would like to be able to pick from a list of like-minded people that I could invite into a conversation.

Walkthrough:
This would be done in two phases. The user would use the app to find a few people with like interests. This would happen by using the “match” functionality to find people, and once the user has been matched with enough people, they can create a group chat. 

For the first phase, the frontend would call a method in API such as “get random potential match”, and either accept or reject by calling accept/reject with the API. If accepted, the API would create a match object between the two users with the match status “pending”, and then pass it to the DOA to create a corresponding entry in the database. To get one of those pending matches on the user’s contact list, the other user has to also accept, and this will change the “pending” status to “matched”. 

Now, assuming the user has a few people in their contact list: The frontend makes a call to getListofMatches , which will interact with the DOA to get a list of Match objects, and that will be passed in some form back to the frontend. Then the user can click on a “create group” button and select some people from list of matches, and from here a call will be made to whichever chat service we will be using to initiate a chat.

User story:
As a shy person, I would like the option to remain anonymous.

Walkthrough:
The frontend web app would call a method in API, such as createAccount which passes in all the profile data, including an “anonymous” flag. The API class would then create a User object with the data, and pass it on to the DAO which would create a corresponding entry in the database. Now whenever a User object is created for this user, the anonymous flag will tell the object to not give out info such as Facebook account details and anything else that would identify the user.
