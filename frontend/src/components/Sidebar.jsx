import { Nav } from 'react-bootstrap'
import { NavLink, useParams } from 'react-router-dom'

export default function Sidebar() {
  const { id } = useParams()
  if (!id) return null

  return (
    <Nav className="flex-column bg-light p-3" style={{ minWidth: 200, minHeight: '100%' }}>
      <Nav.Link as={NavLink} to={`/houses/${id}`} end>Overview</Nav.Link>
      <Nav.Link as={NavLink} to={`/houses/${id}/rooms/new`}>Add Room</Nav.Link>
      <Nav.Link as={NavLink} to={`/houses/${id}/devices/new`}>Add Device</Nav.Link>
    </Nav>
  )
}
