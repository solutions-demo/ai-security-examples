# 6. Package model governance

Package models are model files, such as open-weight models from Hugging Face, that developers download
and load into their own code. Two things make that risky. Loading a model can run code: formats such as Pickle execute
instructions as the file is read. And every popular foundation model has hundreds or thousands of
fine-tuned variants, many with ambiguous licensing, questionable provenance, or too few users for the
community to have vetted them. In this guide you find models pulled outside governance (Shadow AI), block
one, catch a malicious one, spot a model baked into a container image, and build an approved list of
models for a project.

This guide is about **model weights**: model files stored in and served through Artifactory. It doesn't
cover hosted model APIs such as OpenAI or Gemini.

> [!IMPORTANT]
> Before you start, complete [access and authentication](03-access-and-auth.md): the developer user and the
> JFrog CLI are used throughout. JFrog AI Security enforces model decisions through JFrog Curation, so Curation
> must be active and turned on ([prerequisites](01-prerequisites.md#turn-on-curation)), then enabled for
> your Hugging Face repositories.

## How model governance works

| Step | What JFrog does |
|------|-----------------|
| **Find** | Xray indexes your repositories. A model found in a repository that no governed project approved shows up in **Shadow AI**, usually within about an hour. Models baked into container images in Artifactory are found too, because Xray unpacks image layers. |
| **Check** | For Hugging Face models, Xray looks for files that run code when the model loads, across formats such as Pickle, PyTorch, H5, Joblib, Dill and GGUF. JFrog Security Research confirms whether that code is malicious. |
| **Decide** | An admin blocks a model, in one repository or everywhere, or approves it for a project and adds it to the registry. Curation enforces the decision on every download from then on: a blocked model is refused with a 403. |

## Part 1: Set up an ungoverned surface

To play the role of unmonitored AI usage, create two repositories that don't belong to your evaluation
project:

1. Go to **All Projects → Administration → Repositories → Create Repository → Remote → HuggingFace**, name
   it `shadow-model-repo`, and enable **Xray indexing**. It proxies `https://huggingface.co`.
2. Create a **local Docker** repository named `shadow-model-docker-repo`, also with **Xray indexing**
   enabled.

Then give the developer user access, since the repositories sit outside its project:

1. Go to **All Projects → Administration → User Management → Permissions → New Permission**.
2. Under **Repositories**, select both repositories. Under **Users**, add the developer user. Save.

## Part 2: Download a model outside governance

Download a model through the ungoverned repository, as a developer would:

```bash
jf hf download google/flan-t5-small --repo-key=shadow-model-repo --server-id=<YOUR-SERVER>
```

`--repo-key` points the download at the Artifactory repository, and the CLI uses your server's
credentials. Any Hugging Face client works the same way once it's pointed at Artifactory:

```bash
export HF_ENDPOINT=https://<your-instance>.jfrog.io/artifactory/api/huggingfaceml/shadow-model-repo
export HF_TOKEN=<your access token>
```

The model now sits in a repository no governed project owns, so it's recorded as a shadow model. Give it
about an hour to appear in Shadow AI.

> [!TIP]
> Developers downloading straight from huggingface.co bypass Artifactory entirely. The
> [Package Traffic Controller](https://docs.jfrog.com/security/docs/package-traffic-controller) reroutes
> those downloads through Artifactory at the network level. It requires JFrog Curation and a supported SASE
> provider (Zscaler, Cloudflare Gateway or Netskope).

## Part 3: Find the model and block it

1. Open **AI Security → Shadow AI**.
2. Find `google/flan-t5-small`, marked **Unmanaged**, and open it.
3. On the **Found At** tab, find `shadow-model-repo` and click **Block**. **Block everywhere** blocks the
   model in every repository it's found in.

Blocking takes effect within a few minutes and changes the model's status to **Managed**. To confirm it,
clear the local Hugging Face cache and download again:

```bash
rm -rf ~/.cache/huggingface/hub/models--google--flan-t5-small
jf hf download google/flan-t5-small --repo-key=shadow-model-repo --server-id=<YOUR-SERVER>
```

The download is now refused with a **403** from Curation. Without clearing the cache, the client would
reuse the copy it already has.

## Part 4: Catch a malicious model

[`MustEr/gpt2-elite`](https://huggingface.co/MustEr/gpt2-elite) is a known malicious model: its
`pytorch_model.bin` runs code as soon as the model is loaded. It also shows the provenance problem: a
"gpt2" lookalike from an unknown publisher, with only a handful of downloads.

> [!CAUTION]
> Download it only with the command below, and never load it, for example with `from_pretrained()`.
> Downloading stores the files; loading them is what runs the code.

```bash
jf hf download MustEr/gpt2-elite --repo-key=shadow-model-repo --server-id=<YOUR-SERVER>
```

Within about an hour it appears in **Shadow AI** marked **Malicious**. A malicious model can be blocked
but never approved for a project. If your Curation policies already block malicious packages, the download
itself is refused with a 403, and the model never reaches the machine.

## Part 5: Find a model inside a container image

Models also reach production baked into images. This uses the `jfrog-hf-docker-demo` sample from
[jfrog/JFrogMLExamples](https://github.com/jfrog/JFrogMLExamples), which packages `google/flan-t5-small`.

1. Build the image with the model inside:

   ```bash
   cd jfrog-hf-docker-demo/
   ./build-with-local-model.sh
   ```

2. Push it to the shadow Docker repository:

   ```bash
   export ARTIFACTORY_URL=<YOUR-ARTIFACTORY-URL>
   export ARTIFACTORY_REPO=shadow-model-docker-repo
   ./push_to_jfrog.sh
   ```

   If the script fails to authenticate, push with the JFrog CLI instead:

   ```bash
   jf docker push <your-instance>.jfrog.io/shadow-model-docker-repo/jfrog-hf-demo:latest --server-id <YOUR-SERVER>
   ```

3. Open `google/flan-t5-small` in **Shadow AI** again. It now shows **Partially Managed**: blocked in
   `shadow-model-repo`, but also found in `shadow-model-docker-repo`, with the image path under **Found At**.

## Part 6: Build an approved list of models

Blocking deals with one model at a time. The lasting answer is an approved list per project, so developers
use vetted models rather than whichever fine-tune they come across. Here you approve `flan-t5-small`
without blocking the repositories:

1. Assign both shadow repositories to your evaluation project. For each one, go to **Administration →
   Repositories**, click the three dots at the right of its row, choose **Project Assignment**, select
   your project and click **Assign**.
2. Go to **AI Security → Marketplace → Models** and search for `flan-t5-small`.
3. Click **Add to Registry**, choose **Allow in project**, select your evaluation project and click
   **Allow**. Then click **View in Registry**.

The model is now in the project's registry. Its page shows its scan results and an **ML-BOM** tab, which
lists what the model is made of and can be exported as CycloneDX or SPDX.

## Troubleshooting

- **A downloaded model doesn't show in Shadow AI:** it usually takes about an hour. Check that the
  repository is indexed by Xray (**Administration → Xray Settings → Indexed Resources**).
- **A blocked model still downloads:** clear the local Hugging Face cache, and check that Curation is on
  for the remote repository.
- **The model isn't in the Marketplace:** only an admin can allow models, and none are allowed by default.

See also: [Get started with AI models](https://docs.jfrog.com/ai-ml/docs/ai-catalog-quick-start) ·
[Shadow AI](https://docs.jfrog.com/ai-ml/docs/detect-shadow-ai) ·
[Discover and allow models](https://docs.jfrog.com/ai-ml/docs/discover-and-allow-models) ·
[Malicious model detection](https://docs.jfrog.com/security/docs/detect-malicious-ai-models) ·
[Hugging Face repositories](https://docs.jfrog.com/artifactory/docs/hugging-face-repositories) ·
[Hugging Face with the JFrog CLI](https://docs.jfrog.com/artifactory/docs/use-hugging-face-with-jfrog-cli) ·
[ML-BOM](https://docs.jfrog.com/ai-ml/docs/ml-bom-overview)

---

**Previous:** [← 5. Agent skill governance](05-agent-skills.md)
