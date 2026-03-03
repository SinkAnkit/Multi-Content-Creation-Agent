import { EventConfig, Handlers } from 'motia'
import { z } from 'zod'
import axios from 'axios'
import * as fs from 'fs'
import * as path from 'path'

const appConfig = require('../config')

const typefullyApiUrl = 'https://api.typefully.com/v1/drafts/'
const headers = {
    'Authorization': `Bearer ${appConfig.typefully.apiKey}`,
    'Content-Type': 'application/json'
}

export const config: EventConfig = {
    type: 'event',
    name: 'ScheduleLinkedin',
    description: 'Schedules generated LinkedIn post using Typefully',
    subscribes: ['linkedin-schedule'],
    emits: [],
    input: z.object({
        requestId: z.string(),
        url: z.string().url(),
        title: z.string(),
        content: z.any(),
        metadata: z.any().optional()
    }),
    flows: ['content-generation']
}

export const handler: Handlers['ScheduleLinkedin'] = async (input, { emit, state, logger }) => {
    try {
        logger.info(`💼 Scheduling LinkedIn post...`)

        // Format the post content
        let linkedinPost = ''
        if (input.content?.post) {
            linkedinPost = input.content.post
        } else if (typeof input.content === 'string') {
            linkedinPost = input.content
        } else {
            linkedinPost = JSON.stringify(input.content, null, 2)
        }

        // Save locally as backup
        const outputDir = path.join(process.cwd(), 'output')
        if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true })
        const filename = `linkedin-post-${input.requestId.slice(0, 8)}-${Date.now()}.md`
        fs.writeFileSync(path.join(outputDir, filename), `# LinkedIn Post: ${input.title}\n\n${linkedinPost}`, 'utf-8')
        logger.info(`💾 Backup saved to: output/${filename}`)

        // Post to Typefully as draft
        const linkedinPayload = {
            content: linkedinPost,
            schedule_date: null
        }

        await axios.post(typefullyApiUrl, linkedinPayload, { headers })

        logger.info(`✅ LinkedIn post scheduled on Typefully!`)
        logger.info(`👀 Visit https://typefully.com/drafts to review and publish!`)

    } catch (error: any) {
        logger.error(`❌ LinkedIn scheduling failed: ${error.message}`)
        logger.info(`💾 Content was still saved locally in output/ folder`)
    }
}
