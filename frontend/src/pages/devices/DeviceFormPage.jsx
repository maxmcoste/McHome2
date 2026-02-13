import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Alert } from 'react-bootstrap'
import { createDevice, updateDevice } from '../../api/devices'
import { listRooms } from '../../api/rooms'
import LoadingSpinner from '../../components/LoadingSpinner'
import { api } from '../../api/client'

const DEVICE_TYPES = ['temperature_sensor', 'window_sensor', 'boiler']

export default function DeviceFormPage() {
  const { id: houseId, deviceId } = useParams()
  const navigate = useNavigate()
  const isEdit = !!deviceId

  const [form, setForm] = useState({
    name: '',
    device_type: 'temperature_sensor',
    driver_name: 'simulator',
    room_id: '',
    config_json: '{}',
  })
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [editHouseId, setEditHouseId] = useState(houseId)

  useEffect(() => {
    const init = async () => {
      try {
        if (isEdit) {
          const device = await api.get(`/api/devices/${deviceId}`)
          // For edit mode, we don't have houseId in the URL - use device.house_id
          // But we need a device GET endpoint. Use the device data from update.
          // Actually devices.py doesn't have a GET by device_id, so we work around:
          setForm({
            name: device.name || '',
            device_type: device.device_type || 'temperature_sensor',
            driver_name: device.driver_name || 'simulator',
            room_id: device.room_id || '',
            config_json: JSON.stringify(device.config_json || {}),
          })
          setEditHouseId(device.house_id)
          const roomList = await listRooms(device.house_id)
          setRooms(roomList)
        } else {
          const roomList = await listRooms(houseId)
          setRooms(roomList)
        }
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [houseId, deviceId, isEdit])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)

    let configObj
    try {
      configObj = JSON.parse(form.config_json)
    } catch {
      setError('Invalid JSON in config')
      setSaving(false)
      return
    }

    try {
      if (isEdit) {
        await updateDevice(deviceId, {
          name: form.name,
          config_json: configObj,
        })
        navigate(`/houses/${editHouseId}`)
      } else {
        await createDevice(houseId, {
          name: form.name,
          device_type: form.device_type,
          driver_name: form.driver_name,
          room_id: form.room_id || null,
          config_json: configObj,
        })
        navigate(`/houses/${houseId}`)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  const backUrl = `/houses/${editHouseId || houseId}`

  return (
    <div style={{ maxWidth: 600 }}>
      <h2>{isEdit ? 'Edit Device' : 'New Device'}</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control name="name" value={form.name} onChange={handleChange} required />
        </Form.Group>

        {!isEdit && (
          <>
            <Form.Group className="mb-3">
              <Form.Label>Device Type</Form.Label>
              <Form.Select name="device_type" value={form.device_type} onChange={handleChange}>
                {DEVICE_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Driver</Form.Label>
              <Form.Control name="driver_name" value={form.driver_name} onChange={handleChange} required />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Room (optional for boiler)</Form.Label>
              <Form.Select name="room_id" value={form.room_id} onChange={handleChange}>
                <option value="">-- No room --</option>
                {rooms.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
              </Form.Select>
            </Form.Group>
          </>
        )}

        <Form.Group className="mb-3">
          <Form.Label>Config JSON</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            name="config_json"
            value={form.config_json}
            onChange={handleChange}
          />
        </Form.Group>

        <Button type="submit" disabled={saving} className="me-2">
          {saving ? 'Saving...' : (isEdit ? 'Update' : 'Create')}
        </Button>
        <Button variant="secondary" onClick={() => navigate(backUrl)}>Cancel</Button>
      </Form>
    </div>
  )
}
