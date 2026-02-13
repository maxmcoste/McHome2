import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Alert } from 'react-bootstrap'
import { createHouse, getHouse, updateHouse } from '../../api/houses'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function HouseFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = !!id

  const [form, setForm] = useState({
    name: '',
    latitude: '',
    longitude: '',
    timezone: 'UTC',
  })
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (isEdit) {
      getHouse(id).then((h) => {
        setForm({
          name: h.name,
          latitude: String(h.latitude),
          longitude: String(h.longitude),
          timezone: h.timezone,
        })
        setLoading(false)
      }).catch((e) => {
        setError(e.message)
        setLoading(false)
      })
    }
  }, [id, isEdit])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    const payload = {
      name: form.name,
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
      timezone: form.timezone,
    }
    try {
      if (isEdit) {
        await updateHouse(id, payload)
      } else {
        await createHouse(payload)
      }
      navigate('/houses')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div style={{ maxWidth: 600 }}>
      <h2>{isEdit ? 'Edit House' : 'New House'}</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control name="name" value={form.name} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Latitude</Form.Label>
          <Form.Control name="latitude" type="number" step="any" value={form.latitude} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Longitude</Form.Label>
          <Form.Control name="longitude" type="number" step="any" value={form.longitude} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Timezone</Form.Label>
          <Form.Control name="timezone" value={form.timezone} onChange={handleChange} required />
        </Form.Group>
        <Button type="submit" disabled={saving} className="me-2">
          {saving ? 'Saving...' : (isEdit ? 'Update' : 'Create')}
        </Button>
        <Button variant="secondary" onClick={() => navigate('/houses')}>Cancel</Button>
      </Form>
    </div>
  )
}
