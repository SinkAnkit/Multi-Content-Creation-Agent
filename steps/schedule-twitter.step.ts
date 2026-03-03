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
    name: 'ScheduleTwitter',
    description: 'Schedules generated Twitter post using Typefully',
    subscribes: ['twitter-schedule'],
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

export const handler: Handlers['ScheduleTwitter'] = async (input, { emit, state, logger }) => {
    try {
        logger.info(`📱 Scheduling Twitter thread...`)

        // Format the thread content
        let twitterThread = ''
        if (input.content?.thread && Array.isArray(input.content.thread)) {
            twitterThread = input.content.thread.map((tweet: any) => tweet.content).join('\n\n\n\n')
        } else if (typeof input.content === 'string') {
            twitterThread = input.content
        } else {
            twitterThread = JSON.stringify(input.content, null, 2)
        }

        // Save locally as backup
        const outputDir = path.join(process.cwd(), 'output')
        if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true })
        const filename = `twitter-thread-${input.requestId.slice(0, 8)}-${Date.now()}.md`
        fs.writeFileSync(path.join(outputDir, filename), `# Twitter Thread: ${input.title}\n\n${twitterThread}`, 'utf-8')
        logger.info(`💾 Backup saved to: output/${filename}`)

        // Post to Typefully as draft
        const twitterPayload = {
            content: twitterThread,
            schedule_date: null
        }

        await axios.post(typefullyApiUrl, twitterPayload, { headers })

        logger.info(`✅ Twitter thread scheduled on Typefully!`)
        logger.info(`👀 Visit https://typefully.com/drafts to review and publish!`)

    } catch (error: any) {
        logger.error(`❌ Twitter scheduling failed: ${error.message}`)
        logger.info(`💾 Content was still saved locally in output/ folder`)
    }
}
