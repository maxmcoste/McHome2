import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Table, Button } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { listSchedules, deleteSchedule } from '../../api/schedules'
import { getHouse } from '../../api/houses'
import { getRoom } from '../../api/rooms'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'
import ConfirmModal from '../../components/ConfirmModal'
import Breadcrumbs from '../../components/Breadcrumbs'

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const WORKDAYS = [0, 1, 2, 3, 4]
const WEEKENDS = [5, 6]

function formatDays(days) {
  if (!days || days.length === 0) return 'Every day'
  if (days.length === 7) return 'Every day'
  const sorted = [...days].sort()
  if (sorted.length === 5 && WORKDAYS.every((d) => sorted.includes(d))) return 'Workdays'
  if (sorted.length === 2 && WEEKENDS.every((d) => sorted.includes(d))) return 'Weekends'
  return sorted.map((d) => DAY_NAMES[d]).join(', ')
}

export default function ScheduleListPage() {
  const { id: houseId, roomId } = useParams()
  const { data, loading, error, refetch } = useApi(() => listSchedules(houseId, roomId), [houseId, roomId])
  const { data: house } = useApi(() => getHouse(houseId), [houseId])
  const { data: room } = useApi(() => getRoom(houseId, roomId), [houseId, roomId])
  const [deleting, setDeleting] = useState(null)

  const handleDelete = async () => {
    try {
      await deleteSchedule(houseId, roomId, deleting)
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
      <Breadcrumbs items={[
        { label: 'Houses', to: '/houses' },
        { label: house?.name || 'House', to: `/houses/${houseId}` },
        { label: room?.name || 'Room' },
        { label: 'Schedules' },
      ]} />
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Schedules</h2>
        <div>
          <Button as={Link} to={`/houses/${houseId}/rooms/${roomId}/schedules/new`} className="me-2">Add Schedule</Button>
          <Button as={Link} to={`/houses/${houseId}`} variant="secondary">Back</Button>
        </div>
      </div>

      <Table striped hover>
        <thead>
          <tr>
            <th>Days</th>
            <th>Start</th>
            <th>End</th>
            <th>Target Temp (C)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {(data || []).map((s) => (
            <tr key={s.id}>
              <td>{formatDays(s.days_of_week)}</td>
              <td>{s.time_start}</td>
              <td>{s.time_end}</td>
              <td>{s.desired_temp_c}</td>
              <td>
                <Button size="sm" variant="outline-danger" onClick={() => setDeleting(s.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      <ConfirmModal
        show={!!deleting}
        title="Delete Schedule"
        message="Are you sure you want to delete this schedule?"
        onConfirm={handleDelete}
        onCancel={() => setDeleting(null)}
      />
    </div>
  )
}
