import { createRoute } from '@tanstack/react-router';
import { rootRoute } from './rootRoute';
import GroupDetails from '../components/GroupDetails';

export const groupDetailsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/groups/$groupId',
  component: GroupDetails,
}); 