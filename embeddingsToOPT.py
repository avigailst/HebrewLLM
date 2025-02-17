from transformers import AutoTokenizer, OPTForCausalLM


def your_input_modification(hidden_states):
    return hidden_states


# Load the tokenizer and model
model_name = "facebook/opt-350m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = OPTForCausalLM.from_pretrained(model_name)


class CustomOPTLayer(model.base_model.decoder.layers[0].__class__):
    def forward(self, hidden_states, attention_mask=None, layer_head_mask=None,
                past_key_value=None, output_attentions=None, use_cache=None):
        # Modify hidden_states before passing them to the original forward method
        modified_hidden_states = your_input_modification(hidden_states)
        return super().forward(modified_hidden_states, attention_mask, layer_head_mask,
                               past_key_value, output_attentions, use_cache)


model.base_model.decoder.layers[0] = CustomOPTLayer(model.base_model.decoder.config)

# Encode the input text
inputs = tokenizer("hello", return_tensors="pt")
# Get model output including hidden states
outputs = model(**inputs)
print(outputs)

# class CustomOPTForCausalLM(OPTForCausalLM):
#     def __init__(self, config):
#         super().__init__(config)
#
#     def forward(self, inputs_embeds=None, **kwargs):
#         if inputs_embeds is not None:
#             # Use the provided embeddings as inputs_embeds
#             return super().forward(inputs_embeds=inputs_embeds, **kwargs)
#         else:
#             # Use the original forward method if no custom embeddings are provided
#             return super().forward(**kwargs)

# model_to_use = "350m"
# # config = AutoConfig.from_pretrained(f"facebook/opt-{model_to_use}")
# # custom_model = CustomOPTForCausalLM(config=config)
# tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
#
# model = OPTForCausalLM.from_pretrained(f"facebook/opt-{model_to_use}")
#
# dummy_input = tokenizer("London is the capital of", return_tensors="pt").input_ids
# outputs = model(dummy_input, output_hidden_states=True)
# embedd = outputs.hidden_states[0]
#
# output = model(inputs_embeds=embedd)
#
# k = 2
# generated_ids = output.logits[:, -1, :].topk(k).indices
# generated_text = tokenizer.decode(generated_ids.tolist()[0])
# print("Generated text:", generated_text)


# OPT
# words = ["לונדון היא עיר הבירה של","חתול", "כלב", "אוטו", "ש", "היא"]
# # file = "C:\\Users\\talia\\PycharmProjects\\TranslatorGPT\\output\\short_words_opt_1.csv"
# # df = pd.read_csv(file)
# # start = eval(df['start'][0])
#
# for word in words:
#     custom_embeddings = hebrewLLM.pred(word)
#     # custom_embeddings = np.append(start, custom_embeddings, axis=0)
#
#     # Convert to PyTorch tensor
#     custom_embeddings_tensor = torch.tensor(custom_embeddings, dtype=torch.float)
#
#     # Debugging: Print the hidden size of the model
#     hidden_size = 512 #config.hidden_size
#     print("Model's hidden size:", hidden_size)
#     # Calculate sequence_length
#     sequence_length = custom_embeddings_tensor.shape[1] // hidden_size
#     if custom_embeddings_tensor.shape[1] % hidden_size != 0:
#         print(
#             f"Warning: The total number of features in the embeddings ({custom_embeddings_tensor.shape[1]}) is not a multiple of the model's hidden size ({hidden_size}).")
#
#     # Reshape embeddings
#     custom_embeddings_tensor = custom_embeddings_tensor.view(1, sequence_length, hidden_size)
#
#     # Debugging: Print type and shape
#     print("Type of custom_embeddings:", type(custom_embeddings_tensor))
#     print("Shape of custom_embeddings:", custom_embeddings_tensor.shape)
#
#     # Forward pass
#     output = custom_model(custom_embeddings=custom_embeddings_tensor)
#     print('word: ' + word)
#     # get answer
#     k = 2
#     generated_ids = output.logits[:, -1, :].topk(k).indices
#     # Decode the generated token IDs to text
#     generated_text = tokenizer.decode(generated_ids.tolist()[0])
#     print("Generated text:", generated_text)
#
#     print('\n<-------------------------------------------------------------------------------------->\n')
