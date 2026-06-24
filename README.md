-----
## 관련 레포지토리

본 레포지토리는 전체 프로젝트 중 **어포던스 기반 Adaptive Convex Decomposition 파트**를 구현한 레포지토리입니다.

본 레포지토리에서 사용하는 affordance prediction 및 전처리 결과는 아래 레포지토리에서 생성됩니다.

* **3D Affordance Inference Pipeline**: [Software_Capstone](https://github.com/Ggulbogpig/Software_Capstone)

전체 파이프라인에서 `Software_Capstone` 레포지토리는 3D 객체로부터 point-level 및 face-level affordance label을 추론하는 역할을 수행합니다.
이후 본 `Software_Capstone_Empart` 레포지토리는  산출한 영역별 ACD granularity를반으로, Empart ACD / V-HACD 기반의 interaction-aware convex decomposition을 수행합니다.

## 실행 흐름 및 주요 코드 역할

본 레포지토리는 affordance inference 결과를 입력으로 받아, Empart ACD 기반의 영역별 convex decomposition을 수행하기 위한 실험 코드와 실행 스크립트를 포함합니다.

전체 실행 흐름은 다음과 같습니다.

```text
Affordance Region CSV
        ↓
Region-wise ACD Parameter Setting
        ↓
Empart ACD / V-HACD Decomposition
        ↓
Result JSON 생성
        ↓
GLB / Convex Hull 시각화
```

---

## 주요 파일 역할

| 파일 / 폴더                                   | 역할                                             |
| ----------------------------------------- | ---------------------------------------------- |
| `run_empart.sh`                           | Empart ACD decomposition을 실행하기 위한 shell script |
| `intrinsic/empart/decompose.py`           | Empart ACD의 핵심 decomposition 실행 코드             |
| `intrinsic/empart/decompose_backup.py`    | 수정 전 또는 백업용 decomposition 코드                   |
| `intrinsic/empart/__main__.py`            | `python -m intrinsic.empart ...` 명령어 진입점       |
| `intrinsic/empart/approximation_error.py` | decomposition 결과의 approximation error 계산       |
|                                           |                                                |
| `visualizeCLI.py`                         | CLI 기반 decomposition 결과 시각화                    |
| `visualize_points.py`                     | affordance point cloud 또는 region 결과 시각화        |
| `showglb.py`                              | GLB 결과 파일 확인 및 시각화                             |
| `topoint.py`                              | mesh 또는 결과 데이터를 point 기반 표현으로 변환               |
| `auto_regions_*.csv`                      | affordance-aware bounding box region 입력 파일     |
|                                           |                                                |
|                                           |                                                |

---

## 입력 파일

Empart ACD 실행에는 기본적으로 다음 입력이 필요합니다.

### 1. 3D Mesh 파일

예시:

```text
3465.obj
input.obj
motor.glb
mug8555.obj
microwave3465.obj
```

Mesh 파일은 decomposition 대상 객체입니다.

### 2. Region CSV 파일

Affordance-aware bounding box 정보를 담은 CSV 파일입니다.

예시:

```text
auto_regions.csv
auto_regions_microwave3465.csv
auto_regions_motor_changed.csv
auto_regions_motor_changed2.csv
auto_regions_mug8555.csv
auto_regions_mug_changed.csv
lift_only.csv
```

Region CSV는 affordance inference 결과를 기반으로 생성되며, 각 region에 대해 affordance label, bounding box 범위, granularity, maxConvexHulls, threshold 등의 정보를 포함합니다.

예시 구조:

```text
region_id,affordance,granularity,min_x,min_y,min_z,max_x,max_y,max_z,maxConvexHulls,acdThreshold
```

---

## 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

---

### 2. Empart ACD 직접 실행

Empart ACD는 다음과 같이 Python module 형태로 실행할 수 있습니다.

```bash
python -m intrinsic.empart decompose <input_mesh> <resolution> \
  --boxes_csv <region_csv> \
  --method coacd > <output_result_json>
```

예시:

```bash
python -m intrinsic.empart decompose 3465.obj 408 \
  --boxes_csv auto_regions_microwave3465.csv \
  --method coacd > total_result_microwave3465.json
```

위 명령어는 `3465.obj`를 입력 mesh로 사용하고, `auto_regions_microwave3465.csv`에 정의된 affordance-aware bounding box를 기반으로 region-wise convex decomposition을 수행합니다.

결과는 다음 파일로 저장됩니다.

```text
total_result_microwave3465.json
```

---

### 3. 특정 region만 테스트

특정 affordance region만 테스트하고 싶은 경우 `lift_only.csv`와 같은 단일 region CSV를 사용할 수 있습니다.

```bash
python -m intrinsic.empart decompose input.obj 408 \
  --boxes_csv lift_only.csv \
  --method coacd > result.json
```

출력:

```text
result.json
```

---

### 4. `run_empart.sh`를 이용한 실행

반복적으로 같은 설정을 실행할 경우 `run_empart.sh`를 사용할 수 있습니다.

```bash
bash run_empart.sh
```

또는 Windows 환경에서 Git Bash / WSL을 사용하는 경우:

```bash
./run_empart.sh
```

`run_empart.sh`는 내부적으로 Empart ACD 실행 명령어를 호출하며, 일반적으로 다음과 같은 형태의 명령어를 포함합니다.

```bash
python -m intrinsic.empart decompose <input_mesh> <resolution> \
  --boxes_csv <region_csv> \
  --method coacd > <output_json>
```

따라서 실험 대상 객체나 region CSV를 바꾸려면 `run_empart.sh` 내부의 다음 항목을 수정하면 됩니다.

```bash
<input_mesh>
<resolution>
<region_csv>
<output_json>
```

예시:

```bash
python -m intrinsic.empart decompose 3465.obj 408 \
  --boxes_csv auto_regions_microwave3465.csv \
  --method coacd > total_result_microwave3465.json
```

---

## 출력 결과

실행 후 생성되는 주요 결과 파일은 다음과 같습니다.

| 결과 파일                             | 설명                                   |
| --------------------------------- | ------------------------------------ |
| `result.json`                     | 단일 실험 또는 기본 decomposition 결과         |
| `total_result_microwave3465.json` | microwave 객체에 대한 전체 decomposition 결과 |
| `*_result.json`                   | 객체별 decomposition 결과                 |
| `*.glb`                           | 시각화 가능한 3D 결과 파일                     |
| `*.ply`                           | point cloud 또는 affordance 시각화 결과     |
| `*.log`                           | 실행 중 발생한 로그 또는 에러 기록                 |

단, `.log`, 대용량 `.glb`, `.obj`, `.ply`, Blender binary, 압축 파일 등은 GitHub 저장소에 포함하지 않고 `.gitignore`로 제외합니다.

---

## 결과 시각화

---

### 1. CLI 결과 시각화

```bash
python visualizeCLI.py
```

Empart ACD CLI 실행 결과인 JSON 또는 mesh 데이터를 확인하는 데 사용합니다.

ACD 결과인 total_result_microwave3465.json 을 시각화하는데 사용할 수 있습니다. 

---

### 2. Point 기반 결과 시각화

```bash
python visualize_points.py
```

Affordance point cloud 또는 region별 point 결과를 시각화할 때 사용합니다.

---

## 실험 예시

### Microwave 객체

입력:

```text
3465.obj
auto_regions_microwave3465.csv
```

실행:

```bash
python -m intrinsic.empart decompose 3465.obj 408 \
  --boxes_csv auto_regions_microwave3465.csv \
  --method coacd > total_result_microwave3465.json
```

출력:

```text
total_result_microwave3465.json
```

목적:

```text
openable / contain affordance가 탐지된 영역을 기준으로 전자레인지 손잡이 및 내부 공간 주변의 convex decomposition 품질을 확인한다.
```

```text
```

---

## 전체 프로젝트 내 역할

본 레포지토리는 전체 프로젝트에서 **후속 decomposition 파트**에 해당합니다.

```text
Software_Capstone
    └── 3D object affordance inference
    └── point-level affordance prediction
    └── face-level affordance mapping
    └── affordance region CSV 생성

Software_Capstone_Empart
    └── affordance region CSV 입력
    └── region-wise granularity 반영
    └── Empart ACD / V-HACD 실행
    └── interaction-aware convex decomposition 결과 생성
```

관련 affordance inference 레포지토리:

* [Software_Capstone](https://github.com/Ggulbogpig/Software_Capstone)

---

## 주의사항

* Blender 실행 파일, 압축 파일, `.tar.xz`, `.zip` 등 대용량 외부 binary는 GitHub에 업로드하지 않습니다.
* `.env` 파일은 API key나 로컬 설정을 포함할 수 있으므로 반드시 `.gitignore`에 포함해야 합니다.
* `*.log`, `*.json`, `*.glb`, `*.ply`, `*.obj` 등 실험 결과 파일은 필요한 예시만 선별적으로 업로드합니다.
* 대용량 결과물은 GitHub가 아닌 별도 Google Drive 또는 release asset으로 관리하는 것을 권장합니다.










# Empart: Interactive Mesh Simplification

This research project offers a web-based interactive tool for simplifying your meshes into convex shapes with varying error tolerances. 
The project is particularly aimed at finetuning collision geometry for physics simulation and robotics algorithms.

Read our pre-print paper explaining Empart on [arXiv](https://www.arxiv.org/pdf/2509.22847).

-----

## Getting Started

### Prerequisites
  * Ubuntu

Ensure you have these installed:
  * **Node.js**: Download from the [official Node.js website](https://nodejs.org/) or
    
    ```bash
    sudo apt install nodejs npm
    ```

  * **Conda (Anaconda or Miniconda)**: Download Miniconda from the [Conda website](https://docs.conda.io/en/latest/miniconda.html). or
    ```bash
    curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh
    bash ~/Anaconda3-2025.06-0-Linux-x86_64.sh
    ```
### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/intrinsic-opensource/empart.git
    cd empart
    ```
2.  **Set Up Python Environment with Conda:**
    ```bash
    conda create -n empart python=3.11
    conda activate empart
    pip install -r requirements.txt
    ```

3.  **Install Node.js Dependencies:**

    ```bash
    cd tools/interactive-viewer
    npm install
    ```

4. **Install Blender (optional for watertight mesh inputs):**    

    Note: If you are expecting to simplify meshes that are not watertight*, our tool requires blender to compute mesh intersections.
    Install blender from `https://www.blender.org/download/`
    ```
    tar -xf blender-4.5.1-linux-x64.tar.xz
    export PATH="/home/youruser/Downloads/blender-4.5.1-linux-x64:$PATH"
    source ~/.bashrc
    ```

    *A watertight triangle mesh is a closed 2-manifold or equivalently, every edge is shared by two faces.

-----

## Running the Application

```bash
cd tools/interactive-viewer
npm start
```

This command will start a local development server and open the application in your browser.

## Running Tests
Install playwright which is used to replay mouse and web events.
```bash
playwright install
```
Then, run the tests using pytest:
```bash
pytest
```
-----
## Citing Empart

Please include this bibtex entry when citing Empart:
```
@misc{vu2025empartinteractiveconvexdecomposition,
      title={Empart: Interactive Convex Decomposition for Converting Meshes to Parts}, 
      author={Brandon Vu and Shameek Ganguly and Pushkar Joshi},
      year={2025},
      eprint={2509.22847},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2509.22847}, 
}
```

-----

## Acknowledgements
`empart`'s ability to efficiently compute mesh intersections is made possible by amazing open source projects such as [Manifold3d](https://github.com/elalish/manifold) and [Blender](https://www.blender.org/)

