import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Alert, ButtonGroup } from 'react-bootstrap'
import { createSchedule } from '../../api/schedules'
import { getHouse } from '../../api/houses'
import { getRoom } from '../../api/rooms'
import Breadcrumbs from '../../components/Breadcrumbs'

const DAYS = [
  { value: 0, label: 'Mon' },
  { value: 1, label: 'Tue' },
  { value: 2, label: 'Wed' },
  { value: 3, label: 'Thu' },
  { value: 4, label: 'Fri' },
  { value: 5, label: 'Sat' },
  { value: 6, label: 'Sun' },
]

const WORKDAYS = [0, 1, 2, 3, 4]
const WEEKENDS = [5, 6]

export default function ScheduleFormPage() {
  const { id: houseId, roomId } = useParams()
  const navigate = useNavigate()

  const [selectedDays, setSelectedDays] = useState([])
  const [form, setForm] = useState({
    time_start: '08:00:00',
    time_end: '22:00:00',
    desired_temp_c: '20',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [houseName, setHouseName] = useState('')
  const [roomName, setRoomName] = useState('')

  useEffect(() => {
    Promise.all([getHouse(houseId), getRoom(houseId, roomId)]).then(([h, r]) => {
      setHouseName(h.name)
      setRoomName(r.name)
    }).catch(() => {})
  }, [houseId, roomId])

  const toggleDay = (day) => {
    setSelectedDays((prev) =>
      prev.includes(day) ? prev.filter((d) => d !== day) : [...prev, day].sort()
    )
  }

  const setPreset = (days) => {
    setSelectedDays([...days])
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await createSchedule(houseId, roomId, {
        days_of_week: selectedDays.length > 0 ? selectedDays : null,
        time_start: form.time_start,
        time_end: form.time_end,
        desired_temp_c: parseFloat(form.desired_temp_c),
      })
      navigate(`/houses/${houseId}/rooms/${roomId}/schedules`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const isAllSelected = selectedDays.length === 7
  const isWorkdays = WORKDAYS.every((d) => selectedDays.includes(d)) && selectedDays.every((d) => WORKDAYS.includes(d))
  const isWeekends = WEEKENDS.every((d) => selectedDays.includes(d)) && selectedDays.every((d) => WEEKENDS.includes(d))

  return (
    <div style={{ maxWidth: 600 }}>
      <Breadcrumbs items={[
        { label: 'Houses', to: '/houses' },
        { label: houseName || 'House', to: `/houses/${houseId}` },
        { label: roomName || 'Room' },
        { label: 'Schedules', to: `/houses/${houseId}/rooms/${roomId}/schedules` },
        { label: 'New' },
      ]} />
      <h2>New Schedule</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Days</Form.Label>
          <div className="mb-2">
            <ButtonGroup size="sm" className="me-2">
              <Button
                type="button"
                variant={selectedDays.length === 0 ? 'primary' : 'outline-primary'}
                onClick={() => setSelectedDays([])}
              >
                Every day
              </Button>
              <Button
                type="button"
                variant={isWorkdays ? 'primary' : 'outline-primary'}
                onClick={() => setPreset(WORKDAYS)}
              >
                Workdays
              </Button>
              <Button
                type="button"
                variant={isWeekends ? 'primary' : 'outline-primary'}
                onClick={() => setPreset(WEEKENDS)}
              >
                Weekends
              </Button>
              <Button
                type="button"
                variant={isAllSelected ? 'primary' : 'outline-primary'}
                onClick={() => setPreset([0, 1, 2, 3, 4, 5, 6])}
              >
                All
              </Button>
            </ButtonGroup>
          </div>
          <div className="d-flex gap-3 flex-wrap">
            {DAYS.map((day) => (
              <Form.Check
                key={day.value}
                type="checkbox"
                id={`day-${day.value}`}
                label={day.label}
                checked={selectedDays.includes(day.value)}
                onChange={() => toggleDay(day.value)}
              />
            ))}
          </div>
          <Form.Text className="text-muted">
            No days selected = applies every day
          </Form.Text>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Start Time</Form.Label>
          <Form.Control name="time_start" type="time" step="1" value={form.time_start} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>End Time</Form.Label>
          <Form.Control name="time_end" type="time" step="1" value={form.time_end} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Desired Temperature (C)</Form.Label>
          <Form.Control name="desired_temp_c" type="number" step="0.5" min="5" max="35" value={form.desired_temp_c} onChange={handleChange} required />
        </Form.Group>
        <Button type="submit" disabled={saving} className="me-2">
          {saving ? 'Saving...' : 'Create'}
        </Button>
        <Button type="button" variant="secondary" onClick={() => navigate(`/houses/${houseId}/rooms/${roomId}/schedules`)}>Cancel</Button>
      </Form>
    </div>
  )
}
