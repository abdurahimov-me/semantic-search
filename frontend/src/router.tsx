import { createRootRoute, createRoute, createRouter } from '@tanstack/react-router'
import { AppShell } from './components/AppShell'
import { DocumentsPage } from './pages/DocumentsPage'
import { TestPage } from './pages/TestPage'

const rootRoute = createRootRoute({ component: AppShell })
const documentsRoute = createRoute({ getParentRoute: () => rootRoute, path: '/', component: DocumentsPage })
const testRoute = createRoute({ getParentRoute: () => rootRoute, path: '/test', component: TestPage })
const routeTree = rootRoute.addChildren([documentsRoute, testRoute])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
