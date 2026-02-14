import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Alert } from 'react-bootstrap'
import { createRoom, getRoom, updateRoom } from '../../api/rooms'
import { getHouse } from '../../api/houses'
import LoadingSpinner from '../../components/LoadingSpinner'
import Breadcrumbs from '../../components/Breadcrumbs'

const ORIENTATIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

export default function RoomFormPage() {
  const { id: houseId, roomId } = useParams()
  const navigate = useNavigate()
  const isEdit = !!roomId

  const [form, setForm] = useState({
    name: '',
    volume_m3: '50',
    insulation_factor: '0.5',
    orientation: 'S',
    window_area_m2: '2',
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [houseName, setHouseName] = useState('')

  useEffect(() => {
    const init = async () => {
      try {
        const house = await getHouse(houseId)
        setHouseName(house.name)
        if (isEdit) {
          const r = await getRoom(houseId, roomId)
          setForm({
            name: r.name,
            volume_m3: String(r.volume_m3),
            insulation_factor: String(r.insulation_factor),
            orientation: r.orientation,
            window_area_m2: String(r.window_area_m2),
          })
        }
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [houseId, roomId, isEdit])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    const payload = {
      name: form.name,
      volume_m3: parseFloat(form.volume_m3),
      insulation_factor: parseFloat(form.insulation_factor),
      orientation: form.orientation,
      window_area_m2: parseFloat(form.window_area_m2),
    }
    try {
      if (isEdit) {
        await updateRoom(houseId, roomId, payload)
      } else {
        await createRoom(houseId, payload)
      }
      navigate(`/houses/${houseId}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  const crumbs = isEdit
    ? [
        { label: 'Houses', to: '/houses' },
        { label: houseName || 'House', to: `/houses/${houseId}` },
        { label: form.name || 'Room' },
        { label: 'Edit' },
      ]
    : [
        { label: 'Houses', to: '/houses' },
        { label: houseName || 'House', to: `/houses/${houseId}` },
        { label: 'New Room' },
      ]

  return (
    <div style={{ maxWidth: 600 }}>
      <Breadcrumbs items={crumbs} />
      <h2>{isEdit ? 'Edit Room' : 'New Room'}</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control name="name" value={form.name} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Volume (m3)</Form.Label>
          <Form.Control name="volume_m3" type="number" step="any" value={form.volume_m3} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Insulation Factor (0-1)</Form.Label>
          <Form.Control name="insulation_factor" type="number" step="0.1" min="0" max="1" value={form.insulation_factor} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Orientation</Form.Label>
          <Form.Select name="orientation" value={form.orientation} onChange={handleChange}>
            {ORIENTATIONS.map((o) => <option key={o} value={o}>{o}</option>)}
          </Form.Select>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Window Area (m2)</Form.Label>
          <Form.Control name="window_area_m2" type="number" step="any" value={form.window_area_m2} onChange={handleChange} required />
        </Form.Group>
        <Button type="submit" disabled={saving} className="me-2">
          {saving ? 'Saving...' : (isEdit ? 'Update' : 'Create')}
        </Button>
        <Button variant="secondary" onClick={() => navigate(`/houses/${houseId}`)}>Cancel</Button>
      </Form>
    </div>
  )
}
