import { useParams, Link } from 'react-router-dom'
import { Table, Button } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { listRooms } from '../../api/rooms'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'

export default function RoomListPage() {
  const { id } = useParams()
  const { data, loading, error } = useApi(() => listRooms(id), [id])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorAlert message={error} />

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Rooms</h2>
        <Button as={Link} to={`/houses/${id}/rooms/new`}>Add Room</Button>
      </div>

      <Table striped hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Volume (m3)</th>
            <th>Insulation</th>
            <th>Orientation</th>
            <th>Window Area (m2)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {(data || []).map((r) => (
            <tr key={r.id}>
              <td>{r.name}</td>
              <td>{r.volume_m3}</td>
              <td>{r.insulation_factor}</td>
              <td>{r.orientation}</td>
              <td>{r.window_area_m2}</td>
              <td>
                <Button as={Link} to={`/houses/${id}/rooms/${r.id}/edit`} size="sm" variant="outline-primary" className="me-1">Edit</Button>
                <Button as={Link} to={`/houses/${id}/rooms/${r.id}/schedules`} size="sm" variant="outline-info">Schedules</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  )
}
