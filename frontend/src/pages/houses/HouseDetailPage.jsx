import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Card, Row, Col, Table, Button, Badge } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { getHouse } from '../../api/houses'
import { listRooms, deleteRoom } from '../../api/rooms'
import { listDevices, deleteDevice } from '../../api/devices'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'
import ConfirmModal from '../../components/ConfirmModal'
import Breadcrumbs from '../../components/Breadcrumbs'

export default function HouseDetailPage() {
  const { id } = useParams()
  const { data: house, loading: hLoading, error: hError } = useApi(() => getHouse(id), [id])
  const { data: rooms, loading: rLoading, refetch: refetchRooms } = useApi(() => listRooms(id), [id])
  const { data: devices, loading: dLoading, refetch: refetchDevices } = useApi(() => listDevices(id), [id])

  const [deleteTarget, setDeleteTarget] = useState(null) // { type, id, roomId? }

  const handleDelete = async () => {
    if (!deleteTarget) return
    try {
      if (deleteTarget.type === 'room') {
        await deleteRoom(id, deleteTarget.id)
        refetchRooms()
      } else {
        await deleteDevice(deleteTarget.id)
        refetchDevices()
      }
    } catch {
      // ignore
    }
    setDeleteTarget(null)
  }

  if (hLoading || rLoading || dLoading) return <LoadingSpinner />
  if (hError) return <ErrorAlert message={hError} />
  if (!house) return <ErrorAlert message="House not found" />

  return (
    <div>
      <Breadcrumbs items={[
        { label: 'Houses', to: '/houses' },
        { label: house.name },
      ]} />
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>{house.name}</h2>
        <Button as={Link} to={`/houses/${id}/edit`} variant="outline-primary" size="sm">Edit House</Button>
      </div>

      <Row className="mb-2">
        <Col md={4}><strong>Location:</strong> {house.latitude.toFixed(4)}, {house.longitude.toFixed(4)}</Col>
        <Col md={4}><strong>Timezone:</strong> {house.timezone}</Col>
        <Col md={4}>
          <Badge bg="info" className="me-2">Rooms: {house.room_count}</Badge>
          <Badge bg="info">Devices: {house.device_count}</Badge>
        </Col>
      </Row>

      <Card className="mb-4 mt-3">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span>Rooms</span>
          <Button as={Link} to={`/houses/${id}/rooms/new`} size="sm">Add Room</Button>
        </Card.Header>
        <Card.Body>
          {(!rooms || rooms.length === 0) ? (
            <p className="text-muted mb-0">No rooms yet.</p>
          ) : (
            <Table hover size="sm">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Volume (m3)</th>
                  <th>Orientation</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {rooms.map((r) => (
                  <tr key={r.id}>
                    <td>{r.name}</td>
                    <td>{r.volume_m3}</td>
                    <td>{r.orientation}</td>
                    <td>
                      <Button as={Link} to={`/houses/${id}/rooms/${r.id}/edit`} size="sm" variant="outline-primary" className="me-1">Edit</Button>
                      <Button as={Link} to={`/houses/${id}/rooms/${r.id}/schedules`} size="sm" variant="outline-info" className="me-1">Schedules</Button>
                      <Button size="sm" variant="outline-danger" onClick={() => setDeleteTarget({ type: 'room', id: r.id })}>Delete</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>

      <Card className="mb-4">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span>Devices</span>
          <Button as={Link} to={`/houses/${id}/devices/new`} size="sm">Add Device</Button>
        </Card.Header>
        <Card.Body>
          {(!devices || devices.length === 0) ? (
            <p className="text-muted mb-0">No devices yet.</p>
          ) : (
            <Table hover size="sm">
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
                {devices.map((d) => (
                  <tr key={d.id}>
                    <td>{d.name}</td>
                    <td><Badge bg="secondary">{d.device_type}</Badge></td>
                    <td>{d.driver_name}</td>
                    <td>{d.is_active ? 'Yes' : 'No'}</td>
                    <td>
                      <Button as={Link} to={`/devices/${d.id}/edit`} size="sm" variant="outline-primary" className="me-1">Edit</Button>
                      <Button size="sm" variant="outline-danger" onClick={() => setDeleteTarget({ type: 'device', id: d.id })}>Delete</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>

      <ConfirmModal
        show={!!deleteTarget}
        title={`Delete ${deleteTarget?.type}`}
        message="This action cannot be undone. Are you sure?"
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
