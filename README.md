# FitCore - AI-Powered Fitness App (Backend )

## 📌 Project Overview

FitCore is a cross-platform fitness app that offers AI-generated personalised meal plans and premium workout videos. The backend will be built using **Django & Django REST Framework** to serve as a robust API-driven system for both Android and ios clients.

Users will be able to:
- Watch categorised workout videos
- Receive AI-based meal plans
- Track health data via smart devices or manual input
- Subscribe or make one-time purchases for content

---

## 🏋️ FitCore System Architecture Overview
The FitCore app will follow a client-server architecture with several key components:
### 🧩 Key Components
---
### 📱 Client Applications
- **iOS and Android Apps**: Built with **React Native** for cross-platform support.
- **Admin Web Dashboard**: Used for managing content, users, and analytics.
---

### 🚪 API Gateway / Load Balancer
- Routes requests to appropriate backend services.
- Handles **authentication**, **rate limiting**, and **request validation**.
- Ensures scalability and load distribution.

---

### 🧠 Backend Services

| Service Name                    | Description                                                              |
|----------------------------------|--------------------------------------------------------------------------|
| **Authentication Service**       | Manages user sign-up, login, tokens, and OAuth.                          |
| **User Profile Service**         | Stores and manages user data, goals, preferences, etc.                   |
| **Content Management Service**   | Allows admins to manage workout videos, meal plans, articles, etc.       |
| **Payment Processing Service**   | Handles subscription billing and in-app purchases.                       |
| **Health Data Integration**      | Syncs with devices like Google Fit and Apple HealthKit.                  |
| **AI Meal Plan Generator**       | Uses Openai API to generate personalised meal plans.                     |
| **Notification Service**         | Sends push, email, and in-app notifications.                             |
| **Analytics Service**            | Tracks user engagement, health trends, and admin reports.                |

---

### ☁️ External Services & Storage

| Component                    | Purpose                                                  |
|------------------------------|----------------------------------------------------------|
| **PostgreSQL Database**       | Relational data storage for core app data.               |
| **AWS S3 / Cloudinary**       | Stores media files like images, videos, and documents.   |
| **OpenAI API**                | Generates AI-driven meal plans and suggestions.          |
| **Payment Gateways**          | Integrates Stripe, PayPal, etc. for handling payments.   |
| **Health Data Providers**     | Syncs data from Google Fit, Apple HealthKit, etc.        |

---

## FitCore - Relational Database Design & Architecture

![ER Diagram](https://github.com/roniahamed/FitCore/blob/master/FitCore%20ERD%20.png)

---
### 📐 Entity Relationship Diagram Overview
#### 🧱 Database Models
- `User`: Stores basic user credentials and serves as the central entity linked to almost all other components.
- `users_profiles`: Contains extended user information like age, weight, height, gender, and fitness goals.
- `HealthData`: Tracks users' health metrics such as heart rate and other measurable health indicators over time.
- `MealPlan`: Stores a user’s daily or AI-generated nutritional plan, including calories, macros (protein, carbs, fats), and date.
- `meal`: Details individual meals within a meal plan, including ingredients, macros, description, recipe, and mealtime.
- `workout`: Defines high-level workout goals, difficulty level, categories, and whether it's a premium plan.
- `WorkoutVideo`: Each workout can include multiple videos with order index, duration, thumbnails, and access settings (free/premium).
- `Subscription`: Stores data about users’ active or past subscription plans, including plan type and validity.
- `Payments`: Logs payment transactions related to subscriptions or other purchases, along with plan details and transaction status.
- `Purchases`: Stores non-subscription purchases like premium workout plans or meal packages.
- `Notification`: Contains app notifications specific to users, such as messages, alerts, or updates.
- `UserWorkoutProgress`: Tracks a user's progress for each workout, including completion timestamp and progress percentage.
---

#### 🔄 Database Relationships 

- `Users` ↔ `UsersProfile`, `HealthData`, `Subscriptions`, `Payments`, `Notifications`, `MealPlan`, `UserWorkoutProgress`, `Purchases`
- `MealPlan` ↔ `Meal` (One-to-Many)
- `Workout` ↔ `WorkoutVideo` (One-to-Many)
- `Users` ↔ `UserWorkoutProgress` (One-to-Many)
- `Workout` ↔ `UserWorkoutProgress` (Many-to-Many through tracking)
- `Workout` ↔ `Purchases` (for purchasing premium content)
- `Users` ↔ `Workout` (via Progress and Purchases)

---
## 📌 API Endpoints

All endpoints are categorised by service, along with HTTP methods, descriptions, and estimated implementation times.

---

### 🔐 Authentication Service

| Endpoint                           | Method | Description               | Time Estimate |
| ---------------------------------- | ------ | ------------------------- | ------------- |
| `/api/auth/register`               | POST   | Register a new user       | 1 day         |
| `/api/auth/login`                  | POST   | Login with email/password | 1 day         |
| `/api/auth/social/google`          | POST   | Google OAuth login        | 1.5 days      |
| `/api/auth/social/apple`           | POST   | Apple OAuth login         | 1.5 days      |
| `/api/auth/refresh-token`          | POST   | Refresh JWT token         | 0.5 day       |
| `/api/auth/password-reset`         | POST   | Request password reset    | 1 day         |
| `/api/auth/password-reset/confirm` | POST   | Confirm password reset    | 1 day         |

---

### 👤 User Service

| Endpoint                   | Method | Description                      | Time Estimate |
| -------------------------- | ------ | -------------------------------- | ------------- |
| `/api/users/profile`       | GET    | Get user profile                 | 0.5 day       |
| `/api/users/profile`       | PUT    | Update user profile              | 0.5 day       |
| `/api/users/settings`      | GET    | Get user settings                | 0.5 day       |
| `/api/users/settings`      | PUT    | Update user settings             | 0.5 day       |
| `/api/users/progress`      | GET    | Get user fitness progress        | 1 day         |
| `/api/users/favorites`     | GET    | Get user favorite workouts/meals | 0.5 day       |
| `/api/users/favorites`     | POST   | Add to favorites                 | 0.5 day       |
| `/api/users/favorites/:id` | DELETE | Remove from favorites            | 0.5 day       |
| `/api/users/dashboard`     | GET    | Get user dashboard summary       | undefine      |

---

### 🧬 Health Data Service

| Endpoint                        | Method | Description               | Time Estimate |
| ------------------------------- | ------ | ------------------------- | ------------- |
| `/api/health/data`              | GET    | Get user health data      | 1 day         |
| `/api/health/data`              | POST   | Add manual health data    | 1 day         |
| `/api/health/sync/google-fit`   | POST   | Sync with Google Fit      | undefine      |
| `/api/health/sync/apple-health` | POST   | Sync with Apple HealthKit | undefine      |
| `/api/health/metrics`           | GET    | Get user health metrics   | 1 day         |
| `/api/health/goals`             | GET    | Get fitness goals         | 0.5 day       |
| `/api/health/goals`             | PUT    | Update fitness goals      | 0.5 day       |

---

### 🏋️‍♂️  Workouts

| Endpoint                     | Method | Description                | Time Estimate |
| ---------------------------- | ------ | -------------------------- | ------------- |
| `/api/workouts`              | GET    | List workouts with filters | 1 day         |
| `/api/workouts/:id`          | GET    | Get workout details        | 0.5 day       |
| `/api/workouts/categories`   | GET    | Get workout categories     | 0.5 day       |
| `/api/workouts/featured`     | GET    | Get featured workouts      | 0.5 day       |
| `/api/workouts/:id/videos`   | GET    | Get workout videos         | 1 day         |
| `/api/workouts/:id/progress` | POST   | Update workout progress    | 2 day         |
| `/api/workouts/:id/rate`     | POST   | Rate a workout             | 0.5 day       |
| `/api/workouts/search`       | GET    | Search workouts            | 1 day         |

---

### ⚙️  Admin Endpoints

| Endpoint                  | Method | Description                    | Time Estimate |
| ------------------------- | ------ | ------------------------------ | ------------- |
| `/api/admin/workouts`     | GET    | List all workouts (admin)      | 0.5 day       |
| `/api/admin/workouts`     | POST   | Create workout (admin)         | 1 day         |
| `/api/admin/workouts/:id` | PUT    | Update workout (admin)         | 1 day         |
| `/api/admin/workouts/:id` | DELETE | Delete workout (admin)         | 0.5 day       |
| `/api/admin/videos`       | POST   | Upload workout video (admin)   | 1.5 days      |
| `/api/admin/videos/:id`   | PUT    | Update video (admin)           | 1 day         |
| `/api/admin/videos/:id`   | DELETE | Delete video (admin)           | 0.5 day       |
| `/api/admin/users`        | GET    | List users (admin)             | 1 day         |
| `/api/admin/analytics`    | GET    | Get platform analytics (admin) | undefine      |

---

### 🥗 Meal Plan Service - Manual Endpoints

| Endpoint                             | Method       | Description                 | Time Estimate |
|--------------------------------------|--------------|-----------------------------|---------------|
| `/api/meals/plans`                   | POST         | Create a manual meal plan   | 1 days        |
| `/api/meals/plans/:id`               | PUT          | Update meal plan            | 1 day         |
| `/api/meals/plans/:id`               | DELETE       | Cancel user meal plan       | 0.5 day       |


### 🧠 AI Meal Plan Service

| Endpoint                    | Method | Description             | Time Estimate |
| --------------------------- | ------ | ----------------------- | ------------- |
| `/api/meals/plans`          | GET    | Get user meal plans     | .5 day        |
| `/api/meals/plans/generate` | POST   | Generate AI meal plan   | undefine      |
| `/api/meals/plans/:id`      | GET    | Get specific meal plan  | .5 day        |
| `/api/meals/plans/:id`      | DELETE | Delete meal plan        | undefine      |
| `/api/meals/templates`      | GET    | Get meal plan templates | undefine      |
| `/api/meals/foods`          | GET    | Search foods database   | .5 day        |

---

### 💳 Payment Service

| Endpoint                                 | Method | Description               | Time Estimate |
| ---------------------------------------- | ------ | ------------------------- | ------------- |
| `/api/payments/subscriptions`            | GET    | Get user subscriptions    | 0.5 day       |
| `/api/payments/subscriptions`            | POST   | Create subscription       | 2 days        |
| `/api/payments/subscriptions/:id`        | PUT    | Update subscription       | 1 day         |
| `/api/payments/subscriptions/:id/cancel` | POST   | Cancel subscription       | 1 day         |
| `/api/payments/purchases`                | GET    | Get user purchases        | 0.5 day       |
| `/api/payments/purchases`                | POST   | Make one-time purchase    | 2 days        |
| `/api/payments/methods`                  | GET    | Get payment methods       | 0.5 day       |
| `/api/payments/methods`                  | POST   | Add payment method        | 1 day         |
| `/api/payments/methods/:id`              | DELETE | Remove payment method     | 0.5 day       |
| `/api/payments/webhooks`                 | POST   | Payment provider webhooks | 1.5 days      |

---

### 🔔 Notification Service

| Endpoint                         | Method | Description                         | Time Estimate |
| -------------------------------- | ------ | ----------------------------------- | ------------- |
| `/api/notifications`             | GET    | Get user notifications              | 0.5 day       |
| `/api/notifications/:id/read`    | PUT    | Mark notification as read           | 0.5 day       |
| `/api/notifications/settings`    | GET    | Get notification settings           | 0.5 day       |
| `/api/notifications/settings`    | PUT    | Update notification settings        | 1 day         |
| `/api/notifications/subscribe`   | POST   | Subscribe to push notifications     | 1 day         |
| `/api/notifications/unsubscribe` | POST   | Unsubscribe from push notifications | 0.5 day       |



## 🛒 Monetization

- **Monthly/Yearly Subscription:** Unlock full access
- **One-time Purchase:** Buy specific videos or plans
- **Free Tier:** Access limited features and samples

---

## 🗂️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT, OAuth2
- **AI Integration:** OpenAI API / Custom ML
- **Media:** AWS S3 or Cloudinary
- **Payments:** Google Play Billing, Apple IAP, Stripe (for web)

---
