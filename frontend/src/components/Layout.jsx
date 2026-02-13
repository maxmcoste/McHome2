import { Outlet } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import Navbar from './Navbar'

export default function Layout() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      <Container fluid className="flex-grow-1 py-3">
        <Outlet />
      </Container>
    </div>
  )
}
