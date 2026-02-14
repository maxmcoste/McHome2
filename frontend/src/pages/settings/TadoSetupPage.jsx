import { useState } from 'react'
import { Button, Alert, Card } from 'react-bootstrap'
import { startAuth, completeAuth } from '../../api/tado'
import Breadcrumbs from '../../components/Breadcrumbs'

export default function TadoSetupPage() {
  const [authUrl, setAuthUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [completing, setCompleting] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleStart = async () => {
    setLoading(true)
    setError(null)
    setSuccess(false)
    try {
      const data = await startAuth()
      setAuthUrl(data.url)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleComplete = async () => {
    setCompleting(true)
    setError(null)
    try {
      await completeAuth()
      setSuccess(true)
      setAuthUrl(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setCompleting(false)
    }
  }

  const crumbs = [
    { label: 'Settings', to: '/settings' },
    { label: 'Tado Setup' },
  ]

  return (
    <div style={{ maxWidth: 600 }}>
      <Breadcrumbs items={crumbs} />
      <h2>Tado Setup</h2>
      <p>Connect your Tado account to read temperatures and control heating.</p>

      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">Tado connected successfully!</Alert>}

      {!authUrl && !success && (
        <Button onClick={handleStart} disabled={loading}>
          {loading ? 'Starting...' : 'Connect Tado'}
        </Button>
      )}

      {authUrl && (
        <Card className="mt-3">
          <Card.Body>
            <Card.Title>Authorize McHome2</Card.Title>
            <p>
              Open the link below and sign in with your Tado account:
            </p>
            <p>
              <a href={authUrl} target="_blank" rel="noopener noreferrer">{authUrl}</a>
            </p>
            <p>Once you have authorized the app in your browser, click the button below.</p>
            <Button onClick={handleComplete} disabled={completing}>
              {completing ? 'Completing...' : 'Complete Setup'}
            </Button>
          </Card.Body>
        </Card>
      )}
    </div>
  )
}
