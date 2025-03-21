# EmpathAI Frontend

This is the frontend application for EmpathAI, an advanced AI therapeutic support system that combines emotion recognition, personalized responses, and an intuitive user interface.

## Key Features

- **Home Page**: Information about EmpathAI capabilities and a real-time emotion analyzer demo
- **Dynamic Session Routing**: Each therapy session has a unique URL (`/session/{uuid}`)
- **Real-time Emotion Analysis**: Visualize emotions as you type or speak
- **Voice Input Support**: Record and analyze audio for a more natural interaction
- **Rich Text Responses**: AI responses with Markdown support for better readability
- **Responsive Design**: Optimized for both desktop and mobile devices

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Application Structure

- **Home Page** (`/`): Landing page with information and demo
- **Session Creation** (`/session`): Redirects to a new session with unique ID
- **Therapy Session** (`/session/{uuid}`): Individual therapy conversation session
- **Settings** (`/settings`): Configuration for LLM providers and models

## Dynamic Routes

The application uses Next.js dynamic routes for session management:

- When a user clicks "Start Therapy Session" on the home page, a unique UUID is generated
- The user is redirected to `/session/{uuid}` where the therapy session takes place
- Session IDs are passed to the backend API to enable future session persistence
- Session URLs can be bookmarked or shared for later use

## Components

Key components in the application:

- `HomePage`: Landing page with information and emotion analysis demo
- `TherapySession`: Main component for the therapy conversation interface
- `EmotionVisualizer`: Visual representation of detected emotions
- `Header`: Navigation and branding

## Learn More

To learn more about the technologies used:

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)

## Development

This project uses TypeScript for type safety and follows modern React best practices using hooks and functional components.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
