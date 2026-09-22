import { createFileRoute } from '@tanstack/react-router'
import ProjectsSectionPrototype from '@/components/projects-section-prototype'

export const Route = createFileRoute('/projects')({
  component: ProjectsPage
})

function ProjectsPage() {
  return <ProjectsSectionPrototype />
}
