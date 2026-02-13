import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, ProgressBar, Container } from 'react-bootstrap'
import { useSetup } from '../../context/SetupContext'
import StepDbCheck from './StepDbCheck'
import StepMigrate from './StepMigrate'
import StepCreateHouse from './StepCreateHouse'
import StepComplete from './StepComplete'

const STEPS = ['Database', 'Migrations', 'Create House', 'Complete']

export default function SetupWizard() {
  const [step, setStep] = useState(0)
  const navigate = useNavigate()
  const { setSetupComplete } = useSetup()

  const progress = ((step + 1) / STEPS.length) * 100

  const handleFinish = () => {
    setSetupComplete(true)
    navigate('/')
  }

  return (
    <Container style={{ maxWidth: 700 }} className="mt-5">
      <h2 className="mb-4">McHome2 Setup</h2>
      <ProgressBar now={progress} label={STEPS[step]} className="mb-4" />
      <Card>
        <Card.Body>
          {step === 0 && <StepDbCheck onNext={() => setStep(1)} />}
          {step === 1 && <StepMigrate onNext={() => setStep(2)} />}
          {step === 2 && <StepCreateHouse onNext={() => setStep(3)} />}
          {step === 3 && <StepComplete onFinish={handleFinish} />}
        </Card.Body>
      </Card>
    </Container>
  )
}
