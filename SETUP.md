# Neofetch-style GitHub profile — setup

This makes your GitHub profile look like the terminal/neofetch card (ASCII portrait +
live stats + an "uptime" counter), the same style as `Andrew6rant`'s famous profile.

**How it works:** two SVG files hold the card. A GitHub Action runs `today.py` once a
day, pulls your real stats from GitHub's API, rewrites the numbers into the SVGs, and
commits them back. Your `README.md` embeds those SVGs, so your profile always shows
fresh numbers.

---

## Step 1 — Create the special repo

On GitHub, create a **public** repo named **exactly your username**.
> Example: if your username is `16Teja`, the repo must be `16Teja/16Teja`.

A repo named after your username is what GitHub shows at the top of your profile.

## Step 2 — Put these files in it

Upload/commit everything in this folder to that repo (keep the folder structure):

```
README.md
today.py
dark_mode.svg
light_mode.svg
generate_ascii.py
.github/workflows/build.yaml
cache/requirements.txt
```

## Step 3 — Edit the parts that are yours

1. **`README.md`** — replace all 3 `YourUsername` with your real username.
2. **`dark_mode.svg` and `light_mode.svg`** — edit the text in the `value` tspans:
   `teja@github` header, OS, Host, Kernel (job title), IDE, Languages, Hobbies,
   LinkedIn, GitHub. (Leave the `id="..._data"` numbers alone — the script fills those.)
3. **`today.py`** — set `BIRTHDAY = datetime.datetime(YYYY, M, D)` near the top
   (this drives the "Uptime" line).
4. **The ASCII portrait** (optional but it's the whole point):
   ```
   pip install pillow
   python generate_ascii.py your_photo.jpg
   ```
   Paste the printed `<tspan>` lines over the ASCII block (between `<text x="15" ...>`
   and `</text>`) in **both** SVGs.

## Step 4 — Create a Personal Access Token

The script needs a token to read your stats.

1. GitHub → **Settings → Developer settings → Personal access tokens →
   Fine-grained tokens → Generate new token**.
2. Repository access: **All repositories**.
3. Permissions (Read-only):
   - Repository → **Contents**, **Metadata**, **Commit statuses**, **Pull requests**
   - Account → **Followers**, **Starring**
4. Generate and **copy** the token (starts with `github_pat_...`).

## Step 5 — Add two repo secrets

In the `Username/Username` repo → **Settings → Secrets and variables → Actions →
New repository secret**. Add both:

| Name           | Value                          |
|----------------|--------------------------------|
| `ACCESS_TOKEN` | the token you just copied      |
| `USER_NAME`    | your GitHub username           |

## Step 6 — Run it

Go to the repo's **Actions** tab → enable workflows if prompted → open **README build**
→ **Run workflow**. After ~1–3 minutes it commits updated SVGs. Open your profile —
the card is live. It then refreshes itself daily.

---

### Test locally first (optional)

```powershell
pip install -r cache/requirements.txt
$env:ACCESS_TOKEN = "github_pat_...."
$env:USER_NAME    = "YourUsername"
python today.py
```
Then open `dark_mode.svg` in a browser to preview.

### Troubleshooting
- **Card doesn't change theme** — GitHub caches the raw SVGs via camo; give it a few
  minutes, or hard-refresh.
- **Action fails on `KeyError: 'ACCESS_TOKEN'`** — the secrets in Step 5 aren't set.
- **`403 anti-abuse limit`** — you have a lot of repos/commits; just re-run, the
  `cache/` folder makes later runs fast.
