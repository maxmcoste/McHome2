import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Form, Button, Alert, Card } from 'react-bootstrap'
import { getSettings, updateSettings } from '../../api/settings'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'

export default function SettingsPage() {
  const [form, setForm] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    getSettings().then((s) => {
      setForm(s)
      setLoading(false)
    }).catch((e) => {
      setError(e.message)
      setLoading(false)
    })
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    setSuccess(false)
    try {
      await updateSettings({
        sensor_poll_interval_seconds: parseInt(form.sensor_poll_interval_seconds),
        prediction_interval_seconds: parseInt(form.prediction_interval_seconds),
        prediction_horizon_minutes: parseInt(form.prediction_horizon_minutes),
        reading_retention_days: parseInt(form.reading_retention_days),
        default_boiler_power_watts: parseFloat(form.default_boiler_power_watts),
      })
      setSuccess(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />
  if (error && !form) return <ErrorAlert message={error} />

  return (
    <div style={{ maxWidth: 600 }}>
      <h2>Settings</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">Settings saved!</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Database URL</Form.Label>
          <Form.Control value={form.database_url} disabled />
          <Form.Text className="text-muted">Set via MCHOME2_DATABASE_URL environment variable</Form.Text>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Sensor Poll Interval (seconds)</Form.Label>
          <Form.Control name="sensor_poll_interval_seconds" type="number" value={form.sensor_poll_interval_seconds} onChange={handleChange} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Prediction Interval (seconds)</Form.Label>
          <Form.Control name="prediction_interval_seconds" type="number" value={form.prediction_interval_seconds} onChange={handleChange} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Prediction Horizon (minutes)</Form.Label>
          <Form.Control name="prediction_horizon_minutes" type="number" value={form.prediction_horizon_minutes} onChange={handleChange} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Reading Retention (days)</Form.Label>
          <Form.Control name="reading_retention_days" type="number" value={form.reading_retention_days} onChange={handleChange} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Default Boiler Power (watts)</Form.Label>
          <Form.Control name="default_boiler_power_watts" type="number" step="any" value={form.default_boiler_power_watts} onChange={handleChange} />
        </Form.Group>
        <Button type="submit" disabled={saving}>
          {saving ? 'Saving...' : 'Save Settings'}
        </Button>
      </Form>

      <Card className="mt-4">
        <Card.Body>
          <Card.Title>Integrations</Card.Title>
          <p>
            <Link to="/settings/tado">Tado Setup</Link>
            {' '}&mdash; {form.tado_refresh_token ? 'Connected' : 'Not connected'}
          </p>
        </Card.Body>
      </Card>
    </div>
  )
}
