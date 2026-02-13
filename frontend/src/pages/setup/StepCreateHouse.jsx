import { useState } from 'react'
import { Form, Button, Alert } from 'react-bootstrap'
import { createHouse } from '../../api/houses'

export default function StepCreateHouse({ onNext }) {
  const [form, setForm] = useState({
    name: '',
    latitude: '',
    longitude: '',
    timezone: 'UTC',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await createHouse({
        name: form.name,
        latitude: parseFloat(form.latitude),
        longitude: parseFloat(form.longitude),
        timezone: form.timezone,
      })
      onNext()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <h4>Step 3: Create Your First House</h4>
      <p className="text-muted">Enter the location details for your home.</p>

      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={handleSubmit} style={{ maxWidth: 500 }}>
        <Form.Group className="mb-3">
          <Form.Label>House Name</Form.Label>
          <Form.Control
            name="name"
            value={form.name}
            onChange={handleChange}
            required
            placeholder="My Home"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Latitude</Form.Label>
          <Form.Control
            name="latitude"
            type="number"
            step="any"
            value={form.latitude}
            onChange={handleChange}
            required
            placeholder="41.9028"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Longitude</Form.Label>
          <Form.Control
            name="longitude"
            type="number"
            step="any"
            value={form.longitude}
            onChange={handleChange}
            required
            placeholder="12.4964"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Timezone</Form.Label>
          <Form.Control
            name="timezone"
            value={form.timezone}
            onChange={handleChange}
            required
            placeholder="Europe/Rome"
          />
        </Form.Group>
        <Button type="submit" disabled={saving}>
          {saving ? 'Creating...' : 'Create House'}
        </Button>
      </Form>
    </div>
  )
}
