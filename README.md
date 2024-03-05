
# Django Social Media Project

## Overview

This Django project serves as a comprehensive social media platform, encompassing features such as user authentication, content creation, direct messaging, and user activity tracking.

### Apps

#### 1. Accounts

The `accounts` app manages user profiles, authentication, and the relationship between users such as followers and following.

-**Models:**
  -`Profile`: Represents user profiles with additional information like bio and profile picture.
  -`Follow`: Tracks the follower-following relationship between users.

-**Views:**
  -`SignUpView`: Allows users to sign up for the platform.
  -`LoginView`: Handles user authentication and provides JWT tokens.
  -`ProfileUpdateView`: Enables users to update their profile information.

- ...

#### 2. Content

The `content` app handles the creation and interaction with various types of content, including posts, likes, tags, stories, and more.

-**Models:**
  -`Post`: Represents user posts with titles, captions, and associated media.
  -`Like`: Tracks user likes on posts.
  -`Tag`: Captures user tags on posts.

- ...

-**Views:**
  -`PostViewSet`: Manages CRUD operations for user posts.
  -`AddTagView`, `RemoveTagView`: Add and remove tags from posts.
  -`AddLikeView`, `RemoveLikeView`: Add and remove likes from posts.

- ...

#### 3. Direct

The `direct` app facilitates direct messaging between users.

-**Models:**
  -`Message`: Represents messages between users.
  -`Image`, `Video`, `Audio`: Media attachments for messages.

-**Views:**
  -`SendMessageAPIView`: Allows users to send messages to each other.
  -`UserMessagesAPIView`: Retrieves messages between the authenticated user and a specific user.
  -`AllUserMessagesAPIView`: Retrieves all messages involving the authenticated user.

- ...

#### 4. User Activity

The `user_activity` app manages user interactions, such as comments on posts.

-**Models:**
  -`Comment`: Represents user comments on posts.

-**Views:**
  -`CommentListCreateView`: Lists and creates comments on posts.
  -`CommentDetailView`: Retrieves, updates, and deletes individual comments.

- ...

#### 5. Logger

The `logger` app includes middleware for logging requests and responses.

-**Middleware:**
  -`LoggingMiddleware`: Logs information about requests and responses.

### Installation

To set up and run the project, follow these steps:

1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Apply migrations: `python manage.py migrate`.
4. Run the development server: `python manage.py runserver`.

### Logging Middleware

The `logger` app provides middleware for logging requests and responses. It captures information such as the path, method, status code, user, and elapsed time.

### Directory Structure

/project-root
|-- accounts
|-- content
|-- direct
|-- user_activity
|-- logger
|-- landing_page
|-- media
|-- static
|-- templates
|-- manage.py
|-- requirements.txt
|-- README.md
|-- ...other project files

### Django Rest Framework

This project is built on top of Django Rest Framework (DRF), a powerful and flexible toolkit for building Web APIs in Django. DRF provides a rich set of features, including serialization, authentication, and viewsets, making it an ideal choice for developing API-based applications.

For more information about Django Rest Framework, visit [DRF Documentation](https://www.django-rest-framework.org/).
