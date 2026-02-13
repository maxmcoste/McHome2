import { useParams, Link } from 'react-router-dom'
import { Table, Button, Badge } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { listDevices } from '../../api/devices'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'

export default function DeviceListPage() {
  const { id } = useParams()
  const { data, loading, error } = useApi(() => listDevices(id), [id])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorAlert message={error} />

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Devices</h2>
        <Button as={Link} to={`/houses/${id}/devices/new`}>Add Device</Button>
      </div>

      <Table striped hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Driver</th>
            <th>Active</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {(data || []).map((d) => (
            <tr key={d.id}>
              <td>{d.name}</td>
              <td><Badge bg="secondary">{d.device_type}</Badge></td>
              <td>{d.driver_name}</td>
              <td>{d.is_active ? 'Yes' : 'No'}</td>
              <td>
                <Button as={Link} to={`/devices/${d.id}/edit`} size="sm" variant="outline-primary">Edit</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  )
}
