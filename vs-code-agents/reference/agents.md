# Supported AI models in GitHub Copilot

Learn about the supported AI models in GitHub Copilot.

GitHub Copilot supports multiple models, each with different strengths. Some models prioritize speed and cost-efficiency, while others are optimized for accuracy, reasoning, or working with multimodal inputs (like images and code together).

Depending on your Copilot plan and where you're using it—such as GitHub.com or an IDE—you may have access to different models.

> \[!NOTE]
>
> * Model availability is subject to change. Some models may be replaced or updated over time.
> * In Visual Studio Code you can add more models than those that are available by default with your Copilot subscription. See [Changing the AI model for GitHub Copilot Chat](/en/copilot/how-tos/use-ai-models/change-the-chat-model?tool=vscode#adding-more-models).

For all of the default AI models, input prompts and output completions run through GitHub Copilot's content filters for harmful, offensive, or off-topic content, and for public code matching when enabled.

## Supported AI models in Copilot

This table lists the AI models available in Copilot, along with their release status and availability in different modes.

> \[!Important] Complimentary access to Grok Code Fast 1 is continuing past the previously announced end time. A new end date has not been set. We may update or conclude this promotion at any time. [Regular pricing](/en/copilot/reference/ai-models/supported-models#model-multipliers) applies after the extension ends.

<div class="ghd-tool rowheaders">

| Model name | Provider | Release status | Agent mode | Ask mode | Edit mode |
| ---------- | -------- | -------------- | ---------- | -------- | --------- |
|            |          |                |            |          |           |

</div>

## Model retirement history

The following table lists AI models that are retired or scheduled for retirement from Copilot, along with their retirement dates and suggested alternatives.

<div class="ghd-tool rowheaders">

| Model name | Retirement date | Suggested alternative |
| ---------- | --------------- | --------------------- |
|            |                 |                       |

</div>

## Supported AI models per client

The following table shows which models are available in each client.

> \[!NOTE]
>
> * When you use Copilot Chat in supported IDEs, **Auto** will automatically select the best model for you based on availability. You can manually choose a different model to override this selection. See [About Copilot auto model selection](/en/copilot/concepts/auto-model-selection) and [Changing the AI model for GitHub Copilot Chat](/en/copilot/how-tos/use-ai-models/change-the-chat-model?tool=vscode).
> * GPT-5-Codex is supported in Visual Studio Code v1.104.1 or higher.
> * GPT-5.1-Codex and GPT-5.1-Codex-Mini are supported in:
>   * Visual Studio Code versions 1.104.1 or higher
>   * JetBrains, Copilot plugin versions 1.5.61 or higher
>   * Xcode, Copilot plugin versions 0.45.0 or later
>   * Eclipse, Copilot plugin versions 0.13.0 or later

<div class="ghd-tool rowheaders">

| Model | GitHub.com | Visual Studio Code | Visual Studio | Eclipse | Xcode | JetBrains IDEs |
| ----- | ---------- | ------------------ | ------------- | ------- | ----- | -------------- |
|       |            |                    |               |         |       |                |

</div>

## Supported AI models per Copilot plan

The following table shows which AI models are available in each Copilot plan. For more information about the plans, see [Plans for GitHub Copilot](/en/copilot/about-github-copilot/plans-for-github-copilot).

<div class="ghd-tool rowheaders">

| Available models in chat | Copilot Free | Copilot Pro | Copilot Pro+ | Copilot Business | Copilot Enterprise |
| ------------------------ | ------------ | ----------- | ------------ | ---------------- | ------------------ |
|                          |              |             |              |                  |                    |

</div>

## Model multipliers

Each model has a premium request multiplier, based on its complexity and resource usage. If you are on a paid Copilot plan, your premium request allowance is deducted according to this multiplier.

For more information about premium requests, see [Requests in GitHub Copilot](/en/copilot/managing-copilot/monitoring-usage-and-entitlements/about-premium-requests).

<div class="ghd-tool rowheaders">

| Model | Multiplier for **paid plans** | Multiplier for **Copilot Free** |
| ----- | ----------------------------- | ------------------------------- |
|       |                               |                                 |

</div>

## Next steps

* For task-based guidance on selecting a model, see [AI model comparison](/en/copilot/reference/ai-models/model-comparison).
* To configure which models are available to you, see [Configuring access to AI models in GitHub Copilot](/en/copilot/using-github-copilot/ai-models/configuring-access-to-ai-models-in-copilot).
* To learn how to change your current model, see [Changing the AI model for GitHub Copilot Chat](/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat) or [Changing the AI model for GitHub Copilot inline suggestions](/en/copilot/how-tos/use-ai-models/change-the-completion-model).
* To learn more about Responsible Use and Responsible AI, see [Copilot Trust Center](https://copilot.github.trust.page/) and [Responsible use of GitHub Copilot features](/en/copilot/responsible-use-of-github-copilot-features).
* To learn how Copilot Chat serves different AI models, see [Hosting of models for GitHub Copilot Chat](/en/copilot/reference/ai-models/model-hosting).


# AI model comparison

Compare available AI models in Copilot Chat and choose the best model for your task.

## Comparison of AI models for GitHub Copilot

GitHub Copilot supports multiple AI models with different capabilities. The model you choose affects the quality and relevance of responses by Copilot Chat and Copilot inline suggestions. Some models offer lower latency, while others offer fewer hallucinations or better performance on specific tasks. This guide helps you pick the best model based on your task, not just model names.

> \[!NOTE]
>
> * Different models have different premium request multipliers, which can affect how much of your monthly usage allowance is consumed. For details, see [Requests in GitHub Copilot](/en/copilot/managing-copilot/monitoring-usage-and-entitlements/about-premium-requests).
> * When you use Copilot Chat in supported IDEs, **Auto** will automatically select the best model for you based on availability. You can manually choose a different model to override this selection. See [About Copilot auto model selection](/en/copilot/concepts/auto-model-selection) and [Changing the AI model for GitHub Copilot Chat](/en/copilot/how-tos/use-ai-models/change-the-chat-model?tool=vscode).

### Recommended models by task

> \[!Important] Complimentary access to Grok Code Fast 1 is continuing past the previously announced end time. A new end date has not been set. We may update or conclude this promotion at any time. [Regular pricing](/en/copilot/reference/ai-models/supported-models#model-multipliers) applies after the extension ends.

Use this table to find a suitable model quickly, see more detail in the sections below.

| Model | Task area | Excels at (primary use case) | Further reading |
| ----- | --------- | ---------------------------- | --------------- |
|       |           |                              |                 |

## Task: General-purpose coding and writing

Use these models for common development tasks that require a balance of quality, speed, and cost efficiency. These models are a good default when you don't have specific requirements.

| Model            | Why it's a good fit                                                                                                                             |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-5.1-Codex    | Delivers higher-quality code on complex engineering tasks like features, tests, debugging, refactors, and reviews without lengthy instructions. |
| GPT-5 mini       | Reliable default for most coding and writing tasks. Fast, accurate, and works well across languages and frameworks.                             |
| Grok Code Fast 1 | Specialized for coding tasks. Performs well on code generation, and debugging across multiple languages.                                        |
| Raptor mini      | Specialized for fast, accurate inline suggestions and explanations.                                                                             |

### When to use these models

Use one of these models if you want to:

* Write or review functions, short files, or code diffs.
* Generate documentation, comments, or summaries.
* Explain errors or unexpected behavior quickly.
* Work in a non-English programming environment.

### When to use a different model

If you're working on complex refactoring, architectural decisions, or multi-step logic, consider a model from [Deep reasoning and debugging](#task-deep-reasoning-and-debugging). For faster, simpler tasks like repetitive edits or one-off code suggestions, see [Fast help with simple or repetitive tasks](#task-fast-help-with-simple-or-repetitive-tasks).

## Task: Fast help with simple or repetitive tasks

These models are optimized for speed and responsiveness. They’re ideal for quick edits, utility functions, syntax help, and lightweight prototyping. You’ll get fast answers without waiting for unnecessary depth or long reasoning chains.

### Recommended models

| Model            | Why it's a good fit                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| Claude Haiku 4.5 | Balances fast responses with quality output. Ideal for small tasks and lightweight code explanations. |

### When to use these models

Use one of these models if you want to:

* Write or edit small functions or utility code.
* Ask quick syntax or language questions.
* Prototype ideas with minimal setup.
* Get fast feedback on simple prompts or edits.

### When to use a different model

If you’re working on complex refactoring, architectural decisions, or multi-step logic, see [Deep reasoning and debugging](#task-deep-reasoning-and-debugging).
For tasks that need stronger general-purpose reasoning or more structured output, see [General-purpose coding and writing](#task-general-purpose-coding-and-writing).

## Task: Deep reasoning and debugging

These models are designed for tasks that require step-by-step reasoning, complex decision-making, or high-context awareness. They work well when you need structured analysis, thoughtful code generation, or multi-file understanding.

### Recommended models

| Model           | Why it's a good fit                                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-5 mini      | Delivers deep reasoning and debugging with faster responses and lower resource usage than GPT-5. Ideal for interactive sessions and step-by-step code analysis. |
| GPT-5.2         | Great at complex reasoning, code analysis, and technical decision-making.                                                                                       |
| Claude Sonnet 4 | Improves on 3.7 with more reliable completions and smarter reasoning under pressure.                                                                            |
| Claude Opus 4.5 | Anthropic’s most powerful model. Improves on Claude Opus 4.                                                                                                     |
| Gemini 3 Pro    | Advanced reasoning across long contexts and scientific or technical analysis.                                                                                   |

### When to use these models

Use one of these models if you want to:

* Debug complex issues with context across multiple files.
* Refactor large or interconnected codebases.
* Plan features or architecture across layers.
* Weigh trade-offs between libraries, patterns, or workflows.
* Analyze logs, performance data, or system behavior.

### When to use a different model

For fast iteration or lightweight tasks, see [Fast help with simple or repetitive tasks](#task-fast-help-with-simple-or-repetitive-tasks).
For general development workflows or content generation, see [General-purpose coding and writing](#task-general-purpose-coding-and-writing).

## Task: Working with visuals (diagrams, screenshots)

Use these models when you want to ask questions about screenshots, diagrams, UI components, or other visual input. These models support multimodal input and are well suited for front-end work or visual debugging.

| Model           | Why it's a good fit                                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-5 mini      | Reliable default for most coding and writing tasks. Fast, accurate, and supports multimodal input for visual reasoning tasks. Works well across languages and frameworks. |
| Claude Sonnet 4 | Improves on 3.7 with more reliable completions and smarter reasoning under pressure.                                                                                      |
| Gemini 3 Pro    | Deep reasoning and debugging, ideal for complex code generation, debugging, and research workflows.                                                                       |

### When to use these models

Use one of these models if you want to:

* Ask questions about diagrams, screenshots, or UI components.
* Get feedback on visual drafts or workflows.
* Understand front-end behavior from visual context.

> \[!TIP]
> If you're using a model in a context that doesn’t support image input (like a code editor), you won’t see visual reasoning benefits. You may be able to use an MCP server to get access to visual input indirectly. See [Extending GitHub Copilot Chat with Model Context Protocol (MCP) servers](/en/copilot/customizing-copilot/using-model-context-protocol/extending-copilot-chat-with-mcp).

### When to use a different model

If your task involves deep reasoning or large-scale refactoring, consider a model from [Deep reasoning and debugging](#task-deep-reasoning-and-debugging). For text-only tasks or simpler code edits, see [Fast help with simple or repetitive tasks](#task-fast-help-with-simple-or-repetitive-tasks).

## Next steps

Choosing the right model helps you get the most out of Copilot. If you're not sure which model to use, start with a general-purpose option like GPT-4.1, then adjust based on your needs.

* For detailed model specs and pricing, see [Supported AI models in GitHub Copilot](/en/copilot/using-github-copilot/ai-models/supported-ai-models-in-copilot).
* For more examples of how to use different models, see [Comparing AI models using different tasks](/en/copilot/using-github-copilot/ai-models/comparing-ai-models-using-different-tasks).
* To switch between models, refer to [Changing the AI model for GitHub Copilot Chat](/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat) or [Changing the AI model for GitHub Copilot inline suggestions](/en/copilot/how-tos/use-ai-models/change-the-completion-model).
* To learn how Copilot Chat serves different AI models, see [Hosting of models for GitHub Copilot Chat](/en/copilot/reference/ai-models/model-hosting).


# Hosting of models for GitHub Copilot Chat

Learn how different AI models are hosted for Copilot Chat.

GitHub Copilot can use a variety of AI models. This article explains how these models are hosted and served.

## OpenAI models

Used for:

* GPT-4.1
* GPT-5-Codex (supported in Visual Studio Code v1.104.1 or higher)
* GPT-5 mini
* GPT-5
* GPT-5.1
* GPT-5.1-Codex
* GPT-5.1-Codex-Mini
* GPT-5.1-Codex-Max
* GPT-5.2
* GPT-5.2-Codex

These models are hosted by OpenAI and GitHub's Azure infrastructure.

OpenAI makes the [following data commitment](https://openai.com/enterprise-privacy/): *We \[OpenAI] do not train models on customer business data*. Data processing follows OpenAI's enterprise privacy comments.

GitHub maintains a [zero data retention agreement](https://platform.openai.com/docs/guides/your-data) with OpenAI.

All input requests and output responses processed by GitHub Copilot's models continue to pass through GitHub Copilot's, content filtering systems. These filters include checks for public code matches (when applied) as well as mechanisms to detect and block harmful or offensive content.

## OpenAI models fine-tuned by Microsoft

Used for:

* Raptor mini

Raptor mini is deployed on GitHub managed Azure OpenAI tenant.

## Anthropic models

Used for:

* Claude Haiku 4.5
* Claude Sonnet 4.5
* Claude Opus 4.1
* Claude Opus 4.5
* Claude Sonnet 4

These models are hosted by Amazon Web Services, Anthropic PBC, and Google Cloud Platform. GitHub has provider agreements in place to ensure data is not used for training. Additional details for each provider are included below:

* Amazon Bedrock: Amazon makes the [following data commitments](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html): *Amazon Bedrock doesn't store or log your prompts and completions. Amazon Bedrock doesn't use your prompts and completions to train any AWS models and doesn't distribute them to third parties*.
* Anthropic PBC: GitHub maintains a [zero data retention agreement](https://privacy.anthropic.com/en/articles/8956058-i-have-a-zero-retention-agreement-with-anthropic-what-products-does-it-apply-to) with Anthropic.
* Google Cloud: [Google commits to not training on GitHub data as part of their service terms](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance). GitHub is additionally not subject to prompt logging for abuse monitoring.

To provide better service quality and reduce latency, GitHub uses [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). You can read more about prompt caching on [Anthropic PBC](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching), [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), and [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude-prompt-caching).

When using Claude, input prompts and output completions continue to run through GitHub Copilot's content filters for public code matching, when applied, along with those for harmful or offensive content.

## Google models

Used for:

* Gemini 2.5 Pro
* Gemini 3 Pro
* Gemini 3 Flash

GitHub Copilot uses Gemini 3 Pro, Gemini 3 Flash, and Gemini 2.5 Pro hosted on Google Cloud Platform (GCP). When using Gemini models, prompts and metadata are sent to GCP, which makes the [following data commitment](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance): *Gemini doesn't use your prompts, or its responses, as data to train its models.*

To provide better service quality and reduce latency, GitHub uses [prompt caching](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance#customer_data_retention_and_achieving_zero_data_retention).

When using Gemini models, input prompts and output completions continue to run through GitHub Copilot's content filters for public code matching, when applied, along with those for harmful or offensive content.

## xAI models

> \[!Important] Complimentary access to Grok Code Fast 1 is continuing past the previously announced end time. A new end date has not been set. We may update or conclude this promotion at any time. [Regular pricing](/en/copilot/reference/ai-models/supported-models#model-multipliers) applies after the extension ends.

These models are hosted on xAI. xAI operates Grok Code Fast 1 in GitHub Copilot under a zero data retention API policy. This means xAI commits that user content (both inputs sent to the model and outputs generated by the model):

Will **not** be:

* Logged for any purpose, including human review
* Saved to disk or retained in any form, including as metadata
* Accessible by xAI personnel
* Used for model training

Will **only**:

* Exist temporarily in RAM for the minimum time required to process and respond to each request
* Be immediately deleted from memory once the response is delivered

When using xAI, input prompts and output completions continue to run through GitHub Copilot's content filters for public code matching, when applied, along with those for harmful or offensive content.

For more information, see [xAI's enterprise terms of service](https://x.ai/legal/terms-of-service-enterprise) on the xAI website.