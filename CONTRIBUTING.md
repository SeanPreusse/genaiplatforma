# CONTRIBUTING

So you're looking to contribute to Coherence - that's awesome, we can't wait to see what you do. As a startup with limited headcount and funding, we have grand ambitions to design the most intuitive workflow for building and managing LLM applications. Any help from the community counts, truly.

We need to be nimble and ship fast given where we are, but we also want to make sure that contributors like you get as smooth an experience at contributing as possible. We've assembled this contribution guide for that purpose, aiming at getting you familiarized with the codebase & how we work with contributors, so you could quickly jump to the fun part.

This guide, like Argenti itself, is a constant work in progress. We highly appreciate your understanding if at times it lags behind the actual project, and welcome any feedback for us to improve.

## Installing

### 3. Verify dependencies

Coherencerequires the following dependencies to build, make sure they're installed on your system:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Node.js v18.x (LTS)](http://nodejs.org)
* [pnpm](https://pnpm.io/)
* [Python](https://www.python.org/) version 3.11.x or 3.12.x


### 5. Visit coherence in your browser

To validate your set up, head over to [http://localhost:3000](http://localhost:3000) (the default, or your self-configured URL and port) in your browser. You should now see Coherence up and running.

### Backend

Coherence backend is written in Python using [Flask](https://flask.palletsprojects.com/en/3.0.x/). It uses [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) for task queueing. Authorization logic goes via Flask-login.

```text
[api/]
├── constants             // Constant settings used throughout code base.
├── controllers           // API route definitions and request handling logic.           
├── core                  // Core application orchestration, model integrations, and tools.
├── docker                // Docker & containerization related configurations.
├── events                // Event handling and processing
├── extensions            // Extensions with 3rd party frameworks/platforms.
├── fields                // field definitions for serialization/marshalling.
├── libs                  // Reusable libraries and helpers.
├── migrations            // Scripts for database migration.
├── models                // Database models & schema definitions.
├── services              // Specifies business logic.
├── storage               // Private key storage.      
├── tasks                 // Handling of async tasks and background jobs.
└── tests
```

### Frontend

The website is bootstrapped on [Next.js](https://nextjs.org/) boilerplate in Typescript and uses [Tailwind CSS](https://tailwindcss.com/) for styling. [React-i18next](https://react.i18next.com/) is used for internationalization.

```text
[web/]
├── app                   // layouts, pages, and components
│   ├── (commonLayout)    // common layout used throughout the app
│   ├── (shareLayout)     // layouts specifically shared across token-specific sessions 
│   ├── activate          // activate page
│   ├── components        // shared by pages and layouts
│   ├── install           // install page
│   ├── signin            // signin page
│   └── styles            // globally shared styles
├── assets                // Static assets
├── bin                   // scripts ran at build step
├── config                // adjustable settings and options 
├── context               // shared contexts used by different portions of the app
├── dictionaries          // Language-specific translate files 
├── docker                // container configurations
├── hooks                 // Reusable hooks
├── i18n                  // Internationalization configuration
├── models                // describes data models & shapes of API responses
├── public                // meta assets like favicon
├── service               // specifies shapes of API actions
├── test                  
├── types                 // descriptions of function params and return values
└── utils                 // Shared utility functions
```

## Submitting your PR

At last, time to open a pull request (PR) to our repo. For major features, we first merge them into the `deploy/dev` branch for testing, before they go into the `main` branch. If you run into issues like merge conflicts or don't know how to open a pull request, check out [GitHub's pull request tutorial](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests).
