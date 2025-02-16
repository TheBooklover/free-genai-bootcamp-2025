import * as React from 'react';
import { createRouter, createRootRoute, createRoute } from '@tanstack/react-router';
import { Layout } from './components/Layout';
import GroupDetails from './components/GroupDetails';

const rootRoute = createRootRoute({
  component: Layout,
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: function IndexPage() {
    return React.createElement('div', { className: 'p-4' },
      React.createElement('h1', null, 'Welcome to the Vocabulary App')
    );
  },
});

const groupDetailsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/groups/$groupId',
  component: function GroupDetailsPage() {
    const { groupId } = groupDetailsRoute.useParams();
    return <GroupDetails groupId={parseInt(groupId, 10)} />;
  },
});

const routeTree = rootRoute.addChildren([indexRoute, groupDetailsRoute]);

export const router = createRouter({ routeTree });

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
} 