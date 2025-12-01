import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routes'
import { MainLayout } from './components/layout/MainLayout'

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <AppRoutes />
      </MainLayout>
    </BrowserRouter>
  )
}

export default App
