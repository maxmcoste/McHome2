import { Navbar as BsNavbar, Container, Nav } from 'react-bootstrap'
import { Link, NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <BsNavbar bg="dark" variant="dark" expand="lg" className="mb-0">
      <Container fluid>
        <BsNavbar.Brand as={Link} to="/">McHome2</BsNavbar.Brand>
        <BsNavbar.Toggle aria-controls="main-nav" />
        <BsNavbar.Collapse id="main-nav">
          <Nav className="me-auto">
            <Nav.Link as={NavLink} to="/">Dashboard</Nav.Link>
            <Nav.Link as={NavLink} to="/houses">Houses</Nav.Link>
            <Nav.Link as={NavLink} to="/settings">Settings</Nav.Link>
          </Nav>
        </BsNavbar.Collapse>
      </Container>
    </BsNavbar>
  )
}
