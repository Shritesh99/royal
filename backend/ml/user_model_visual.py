import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def plt_user_learnstyle():
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Load the generated data from CSV files
    skill_level_df = pd.read_csv("skill_level.csv", index_col="ID")
    motivation_df = pd.read_csv("motivation_level.csv", index_col="ID")
    learning_style_df = pd.read_csv("learning_style.csv", index_col="ID")

    # Merge the data into a single DataFrame
    user_df = pd.concat([skill_level_df, motivation_df, learning_style_df], axis=1)

    # Define the subcategories for each learning style feature
    learning_styles = {
        "SI": ["Sensing", "Intuitive"],
        "VV": ["Verbal", "Visual"],
        "AR": ["Active", "Reflective"],
        "SG": ["Sequential", "Global"]
    }

    # Encode the learning style data using one-hot encoding
    for style, subcategories in learning_styles.items():
        for subcategory in subcategories:
            user_df[style + "_" + subcategory] = (user_df[style] == subcategory).astype(int)

    # Compute the count of users for each subcategory within each learning style
    style_counts = pd.DataFrame(columns=["Learning Style", "Subcategory", "Count"])
    for style, subcategories in learning_styles.items():
        for subcategory in subcategories:
            count = user_df[style + "_" + subcategory].sum()
            style_counts = style_counts.append({"Learning Style": style, "Subcategory": subcategory, "Count": count},
                                               ignore_index=True)

    # Create a pivot table of counts for each subcategory by learning style
    pivot_counts = pd.pivot_table(style_counts, values="Count", index="Subcategory", columns="Learning Style")

    # Create the heatmap
    sns.heatmap(pivot_counts, cmap="Blues", annot=True, fmt="g")
    plt.title("Distribution of Learning Styles and Subcategories")
    plt.xlabel("Learning Style")
    plt.ylabel("Subcategory")
    plt.show()

def plt_user_skill():
    # Load the generated data from CSV files
    skill_level_df = pd.read_csv("skill_level.csv", index_col="ID")

    # Define the subcategories for the skill level features
    skill_categories = list(skill_level_df.columns)

    # Compute the count of users for each skill level subcategory
    skill_counts = pd.DataFrame(columns=["Skill Category", "Subcategory", "Count"])
    for category in skill_categories:
        for subcategory in range(11):
            count = (skill_level_df[category] == subcategory).sum()
            skill_counts = skill_counts.append({"Skill Category": category, "Subcategory": subcategory, "Count": count},
                                               ignore_index=True)

    # Create a pivot table of counts for each subcategory by skill category
    pivot_counts = pd.pivot_table(skill_counts, values="Count", index="Subcategory", columns="Skill Category")

    # Create the heatmap
    sns.heatmap(pivot_counts, cmap="Blues", annot=True, fmt="g")
    plt.title("Distribution of Skill Level Categories and Subcategories")
    plt.xlabel("Skill Category")
    plt.ylabel("Subcategory")
    plt.show()

if __name__ == '__main__':
  
        plt_user_learnstyle()
        #plt_user_skill()