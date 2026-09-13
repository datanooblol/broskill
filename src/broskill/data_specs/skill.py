from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class SkillStatus(StrEnum):
    STABLE = 'stable'
    EXPERIMENT = 'experiment'
    DEPRECATED = 'deprecated'

@dataclass
class Skill:
    name:str = field(
        metadata={'description': "a skill name in frontmatter"}
    )
    description:str = field(
        metadata={'description': "a description of the skill in frontmatter"}
    )
    version:str = field(
        metadata={'description': "a skill's version recommending as v0.1.0 (vMajor.Minor.Patch)"}
    )
    path:Path = field(
        metadata={'description': "a directory path of the skill."}
    )
    tags:list[str] | None = field(
        metadata={'description': "tags will use later for searching and filtering"}, 
        default=None
    )
    keywords:list[str] | None = field(
        metadata={'description': "keywords will use later for searching and filtering"}, 
        default=None
    )
    default:bool = field(
        metadata={'description': "default here tells a program that this skill must be loaded or display"}, 
        default=False
    )
    status:SkillStatus | None = field(
        metadata={'description': "status will be: stable if you test it and pass, experiment if you are in developing phase, deprecated if you plan not to use it."}, 
        default=SkillStatus.EXPERIMENT
    )