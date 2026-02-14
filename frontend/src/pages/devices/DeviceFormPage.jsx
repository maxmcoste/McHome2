import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { Form, Button, Alert } from 'react-bootstrap'
import { createDevice, updateDevice } from '../../api/devices'
import { listRooms } from '../../api/rooms'
import { getHouse } from '../../api/houses'
import { listZones } from '../../api/tado'
import LoadingSpinner from '../../components/LoadingSpinner'
import Breadcrumbs from '../../components/Breadcrumbs'
import { api } from '../../api/client'

const DEVICE_TYPES = ['temperature_sensor', 'window_sensor', 'boiler']
const DRIVER_OPTIONS = ['simulator', 'tado']

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
  const [tadoZones, setTadoZones] = useState([])
  const [tadoError, setTadoError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [editHouseId, setEditHouseId] = useState(houseId)
  const [houseName, setHouseName] = useState('')

  useEffect(() => {
    const init = async () => {
      try {
        if (isEdit) {
          const device = await api.get(`/api/devices/${deviceId}`)
          setForm({
            name: device.name || '',
            device_type: device.device_type || 'temperature_sensor',
            driver_name: device.driver_name || 'simulator',
            room_id: device.room_id || '',
            config_json: JSON.stringify(device.config_json || {}),
          })
          setEditHouseId(device.house_id)
          const [roomList, house] = await Promise.all([
            listRooms(device.house_id),
            getHouse(device.house_id),
          ])
          setRooms(roomList)
          setHouseName(house.name)
        } else {
          const [roomList, house] = await Promise.all([
            listRooms(houseId),
            getHouse(houseId),
          ])
          setRooms(roomList)
          setHouseName(house.name)
        }
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [houseId, deviceId, isEdit])

  const loadTadoZones = async () => {
    setTadoError(null)
    try {
      const zones = await listZones()
      setTadoZones(zones)
    } catch (e) {
      setTadoError(e.message)
      setTadoZones([])
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm({ ...form, [name]: value })
    if (name === 'driver_name' && value === 'tado') {
      loadTadoZones()
    }
  }

  const handleZoneChange = (e) => {
    const zoneId = parseInt(e.target.value)
    const zone = tadoZones.find((z) => z.id === zoneId)
    setForm({
      ...form,
      config_json: JSON.stringify({ zone_id: zoneId }),
      name: form.name || (zone ? zone.name : ''),
    })
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

  const effectiveHouseId = editHouseId || houseId
  const crumbs = isEdit
    ? [
        { label: 'Houses', to: '/houses' },
        { label: houseName || 'House', to: `/houses/${effectiveHouseId}` },
        { label: 'Edit Device' },
      ]
    : [
        { label: 'Houses', to: '/houses' },
        { label: houseName || 'House', to: `/houses/${houseId}` },
        { label: 'New Device' },
      ]

  return (
    <div style={{ maxWidth: 600 }}>
      <Breadcrumbs items={crumbs} />
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
              <Form.Select name="driver_name" value={form.driver_name} onChange={handleChange}>
                {DRIVER_OPTIONS.map((d) => <option key={d} value={d}>{d}</option>)}
              </Form.Select>
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

        {form.driver_name === 'tado' ? (
          <Form.Group className="mb-3">
            <Form.Label>Tado Zone</Form.Label>
            {tadoError ? (
              <Alert variant="warning">
                Could not load Tado zones: {tadoError}.{' '}
                <Link to="/settings/tado">Set up Tado</Link> first.
              </Alert>
            ) : tadoZones.length === 0 ? (
              <div>
                <Button variant="outline-secondary" size="sm" onClick={loadTadoZones}>
                  Load Zones
                </Button>
              </div>
            ) : (
              <Form.Select onChange={handleZoneChange} defaultValue="">
                <option value="" disabled>-- Select a zone --</option>
                {tadoZones.map((z) => (
                  <option key={z.id} value={z.id}>{z.name} ({z.type})</option>
                ))}
              </Form.Select>
            )}
          </Form.Group>
        ) : (
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
        )}

        <Button type="submit" disabled={saving} className="me-2">
          {saving ? 'Saving...' : (isEdit ? 'Update' : 'Create')}
        </Button>
        <Button variant="secondary" onClick={() => navigate(backUrl)}>Cancel</Button>
      </Form>
    </div>
  )
}
