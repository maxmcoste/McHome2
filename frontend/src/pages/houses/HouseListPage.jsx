import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Table, Button } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { listHouses, deleteHouse } from '../../api/houses'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'
import ConfirmModal from '../../components/ConfirmModal'

export default function HouseListPage() {
  const { data, loading, error, refetch } = useApi(listHouses)
  const [deleting, setDeleting] = useState(null)

  const handleDelete = async () => {
    try {
      await deleteHouse(deleting)
      setDeleting(null)
      refetch()
    } catch {
      // ignore
    }
  }

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorAlert message={error} />

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Houses</h2>
        <Button as={Link} to="/houses/new">Add House</Button>
      </div>

      <Table striped hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Timezone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {(data || []).map((h) => (
            <tr key={h.id}>
              <td><Link to={`/houses/${h.id}`}>{h.name}</Link></td>
              <td>{h.latitude.toFixed(4)}, {h.longitude.toFixed(4)}</td>
              <td>{h.timezone}</td>
              <td>
                <Button as={Link} to={`/houses/${h.id}/edit`} size="sm" variant="outline-primary" className="me-2">Edit</Button>
                <Button size="sm" variant="outline-danger" onClick={() => setDeleting(h.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      <ConfirmModal
        show={!!deleting}
        title="Delete House"
        message="This will delete the house and all its rooms, devices, and data. Are you sure?"
        onConfirm={handleDelete}
        onCancel={() => setDeleting(null)}
      />
    </div>
  )
}
